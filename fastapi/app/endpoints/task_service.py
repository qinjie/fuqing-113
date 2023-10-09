from fastapi import APIRouter
from models.task_request import TaskRequest, TaskUpdateRequest
from models.response import Response
from models.models import Task, Guest
from db.database import Database
from sqlalchemy import and_, or_, desc

# APIRouter creates path operations for task module
router = APIRouter(
    prefix="/task",
    tags=["Task"],
    responses={404: {"description": "Not found"}},
)

database = Database()
engine = database.get_db_connection()


@router.post("/add")
async def add_task(req: TaskRequest):
    new_task = Task(**vars(req))
    session = database.get_db_session(engine)
    session.add(new_task)
    session.flush()
    # get id of the inserted task
    session.refresh(new_task, attribute_names=['id'])
    data = {'guest_id': new_task.guest_id, "task_id": new_task.id}
    session.commit()
    session.close()
    return Response(data, 200, "Task added successfully.", False)


@router.put("/update")
async def update_task(req: TaskUpdateRequest):
    session = database.get_db_session(engine)
    try:
        new_vals = vars(req)
        new_vals = { k: v for k, v in new_vals.items() if v is not None }        
        is_task_updated = session.query(Task).filter(Task.id == req.id).update(new_vals, synchronize_session=False)
        session.flush()
        session.commit()
        response_msg = "Task updated successfully"
        response_code = 200
        error = False
        if is_task_updated == 1:
            # After successful update, retrieve updated data from db
            data = session.query(Task).filter(
                Task.id == req.id).one()
        elif is_task_updated == 0:
            response_msg = f"No task found with ID: {req.id}"
            error = True
            data = None
        return Response(data, response_code, response_msg, error)
    except Exception as ex:
        print("Error : ", ex)


@router.delete("/delete/{task_id}")
async def delete_task(task_id: str):
    session = database.get_db_session(engine)
    try:
        task = session.query(Task).get(task_id)
        if task:
            session.delete(task)
            session.commit()
            response_msg = "Task deleted successfully"
            response_code = 200
            error = False
            data = {"task_id": task_id}
        else:
            response_msg = f"No task found with ID: {task_id}"
            error = True
            data = None
            response_code = 404
        return Response(data, response_code, response_msg, error)
    except Exception as ex:
        print("Error : ", ex)


@router.get("/{task_id}")
async def read_task(task_id: str):
    session = database.get_db_session(engine)
    response_message = "Task retrieved successfully"
    data = None
    try:
        data = session.query(Task).get(task_id)
    except Exception as ex:
        print("Error", ex)
        response_message = "Task Not found"
    error = False
    return Response(data, 200, response_message, error)


@router.get("/")
async def read_all_tasks(page_size: int=20, page: int=1):
    session = database.get_db_session(engine)
    data = session.query(Task).order_by(
        desc(Task.created_at)).limit(page_size).offset((page-1)*page_size).all()
    return Response(data, 200, "Tasks retrieved successfully.", error=False)

@router.get("/search/{pattern}")
async def read_task(pattern: str):
    session = database.get_db_session(engine)
    data = None
    error = False
    try:
        data = session.query(Task).filter(
            or_(Task.name.like(f'%{pattern}%'), Task.details.like(f'%{pattern}%'))).all()
    except Exception as ex:
        print("Error", ex)
        response_message = "Task Not found"
        error = True
    response_message = "Task retrieved successfully"
    return Response(data, 200, response_message, error)


# Get tasks for a specific guest and order them by 'serial' column
@router.get('/guest/{guest_id}')
def get_guest_tasks(guest_id):
    session = database.get_db_session(engine)
    guest = session.query(Guest).get(guest_id)
    if not guest:
        session.close()
        return Response(None, 404, 'Guest not found', error=True)
    tasks = (
        session.query(Task)
        .filter(Task.guest_id == guest_id)
        .order_by(Task.serial.asc(), Task.date_time.asc())  # Order tasks by 'serial' in ascending order
        .all()
    )
    session.close()
    response_message = f"Tasks for guest {guest_id} retrieved successfully"
    return Response(data=tasks, code=200, message=response_message, error=False)
