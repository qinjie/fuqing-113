from fastapi import APIRouter
from models.guest_request import GuestRequest, GuestUpdateRequest
from models.response import Response
from models.models import Guest, Task
from db.database import Database
from sqlalchemy import and_, or_, desc
from sqlalchemy.orm import joinedload
import hashlib
from uuid import uuid1


# APIRouter creates path operations for guest module
router = APIRouter(
    prefix="/guest",
    tags=["Guest"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()


@router.post("/add")
async def add_guest(req: GuestRequest):
    new_guest = Guest(**vars(req))
    # Generate hash
    random_id = str(uuid1())
    new_guest.hash = hashlib.sha1(random_id.encode("UTF-8")).hexdigest().upper()[:8]
    session = database.get_db_session(engine)
    session.add(new_guest)
    session.flush()
    # Get id of the inserted guest
    session.refresh(new_guest, attribute_names=['id'])
    data = {"guest_id": new_guest.id, 'hash': new_guest.hash}
    session.commit()
    session.close()
    return Response(data, 200, "Guest added successfully.", False)


@router.put("/update")
async def update_guest(req: GuestUpdateRequest):
    session = database.get_db_session(engine)
    try:
        new_vals = vars(req)
        new_vals = { k: v for k, v in new_vals.items() if v is not None }
        is_guest_updated = session.query(Guest).filter(Guest.id == req.id).update(new_vals, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Guest updated successfully"
        response_code = 200
        error = False
        if is_guest_updated == 1:
            # After successful update, retrieve updated data from db
            data = session.query(Guest).filter(Guest.id == req.id).one()
        elif is_guest_updated == 0:
            response_msg = f"No guest found with ID: {req.id}"
            error = True
            data = None
        return Response(data, response_code, response_msg, error)
    except Exception as ex:
        print("Error : ", ex)


@router.delete("/delete/{guest_id}")
async def delete_guest(guest_id: int):
    session = database.get_db_session(engine)
    try:
        is_guest_updated = session.query(Guest).filter(
                and_(Guest.id == guest_id, Guest.is_deleted == False)
            ).update({Guest.is_deleted: True}, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Guest deleted successfully"
        response_code = 200
        error = False
        data = {"guest_id": guest_id}
        if is_guest_updated == 0:
            response_msg = "Guest not deleted. No guest found with this id :" + \
                str(guest_id)
            response_code = 404
            error = True
            data = None
        return Response(data, response_code, response_msg, error)
    except Exception as ex:
        print("Error : ", ex)


@router.get("/{guest_id}")
async def read_guest(guest_id: str):
    session = database.get_db_session(engine)
    response_message = "Guest retrieved successfully"
    data = None
    try:
        data = session.query(Guest).filter(
                and_(Guest.id == guest_id, Guest.is_deleted == False)
            ).options(joinedload(Guest.tasks)).one()
    except Exception as ex:
        print("Error", ex)
        response_message = "Guest Not found"
    error = False
    return Response(data, 200, response_message, error)


@router.get("/hash/{hash}")
async def read_guest(hash: str):
    session = database.get_db_session(engine)
    data = None
    try:
        data = session.query(Guest).filter(
                and_(Guest.hash == hash.upper(), Guest.is_deleted == False)
            ).options(joinedload(Guest.tasks)).one()
        response_message = "Guest retrieved successfully"
    except Exception as ex:
        print("Error", ex)
        response_message = "Guest Not found"
    error = False
    return Response(data, 200, response_message, error)


@router.get("/")
async def read_all_guests(page_size: int=20, page: int=1):
    session = database.get_db_session(engine)
    data = session.query(Guest).filter(and_(Guest.is_deleted == False)).order_by(
        desc(Guest.created_at)).limit(page_size).offset((page-1)*page_size).all()
    return Response(data, 200, "Guests retrieved successfully.", error=False)


@router.get("/search/{pattern}")
async def read_guest(pattern: str):
    session = database.get_db_session(engine)
    data = None
    error = False
    try:
        data = session.query(Guest).filter(
                or_(Guest.full_name.like(f'%{pattern}%'), 
                    Guest.alt_name.like(f'%{pattern}%'),
                    Guest.title.like(f'%{pattern}%'),
                    Guest.organization.like(f'%{pattern}%'))
            ).all()
    except Exception as ex:
        print("Error", ex)
        response_message = "Guest Not found"
        error = True
    response_message = "Guest retrieved successfully"
    return Response(data, 200, response_message, error)

