from fastapi import HTTPException, status

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exists",
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password",
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has expired",
)

TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token is absent",
)

IncorrcetTokenFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrcet token format"
)

UserIsNotPresentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    # detail="", Детали не указываем, чтобы злоумышлиник не брутфорсил backend
)

UserIsNotAdminException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You are not an administrator"
)

RoomCannotBeBookedException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="There are no available rooms"
)

DateFromMoreOrEqualDateToException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="date_from more or equal than date_to"
)

BookingDoesNotExistException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="booking does not exist"
)

LongBookingException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="booking more 30 days"
)
