"""
Generic CRUD router factory.

Most GrowthOS modules (tasks, timetable, skills, goals, journal, projects,
research, startup ideas, reading list) are simple "list of records owned by
a user" resources. Rather than hand-writing five endpoints x nine modules,
this factory builds a standard REST router for any (Model, CreateSchema,
UpdateSchema, OutSchema) tuple, with built-in search/filter/pagination.
"""
from typing import Optional, Type

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app import models


def make_crud_router(
    *,
    prefix: str,
    tag: str,
    model: Type,
    create_schema: Type,
    update_schema: Type,
    out_schema: Type,
    search_fields: Optional[list] = None,
    filter_fields: Optional[list] = None,
):
    router = APIRouter(prefix=prefix, tags=[tag])
    search_fields = search_fields or []
    filter_fields = filter_fields or []

    @router.get("", response_model=list[out_schema])
    def list_items(
        search: Optional[str] = Query(None, description="Free-text search across this module's text fields"),
        status: Optional[str] = Query(None, description="Filter by this module's status/category field, if it has one"),
        page: int = Query(1, ge=1),
        page_size: int = Query(50, ge=1, le=200),
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
    ):
        query = db.query(model).filter(model.user_id == current_user.id)

        if search and search_fields:
            from sqlalchemy import or_
            conditions = [getattr(model, f).ilike(f"%{search}%") for f in search_fields]
            query = query.filter(or_(*conditions))

        if status and filter_fields:
            query = query.filter(getattr(model, filter_fields[0]) == status)

        query = query.order_by(model.id.desc())
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return items

    @router.post("", response_model=out_schema, status_code=201)
    def create_item(
        payload: create_schema,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
    ):
        item = model(**payload.model_dump(), user_id=current_user.id)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @router.get("/{item_id}", response_model=out_schema)
    def get_item(
        item_id: str,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
    ):
        item = db.query(model).filter(model.id == item_id, model.user_id == current_user.id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"{tag} not found")
        return item

    @router.put("/{item_id}", response_model=out_schema)
    def update_item(
        item_id: str,
        payload: update_schema,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
    ):
        item = db.query(model).filter(model.id == item_id, model.user_id == current_user.id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"{tag} not found")
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
        return item

    @router.delete("/{item_id}", status_code=204)
    def delete_item(
        item_id: str,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
    ):
        item = db.query(model).filter(model.id == item_id, model.user_id == current_user.id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"{tag} not found")
        db.delete(item)
        db.commit()
        return None

    return router
