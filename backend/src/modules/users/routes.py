from __future__ import annotations

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users import repository as user_repo
from src.modules.badges import service as badge_service
from src.modules.users.schemas import UserRegisterIn, UserLoginIn, TokenResponse, UserOut, RatingPercentileResponse, UserXPResponse
from src.storages.sql.dependencies import get_db_session
from src.modules.users.dependencies import CurrentUserDep
from src.utils.security import verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация пользователя",
    description="Создает нового пользователя и возвращает JWT токен"
)
async def register(
    data: UserRegisterIn,
    session: AsyncSession = Depends(get_db_session),
) -> TokenResponse:
    """Регистрация нового пользователя"""
    
    # Проверяем, что пользователь с таким email не существует
    existing_user = await user_repo.get_user_by_email(session, data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    try:
        # Создаем пользователя
        user = await user_repo.create_user(
            session,
            email=data.email,
            password=data.password,
            full_name=data.full_name,
            role=data.role,
        )
        
        # Проверяем и выдаем бейджи при регистрации
        await badge_service.badge_service.check_and_award_badges(
            session, user.id, "user_registered"
        )
        await session.commit()
        
        # Создаем токен
        access_token = create_access_token(data={"sub": str(user.id)})
        
        return TokenResponse(
            access_token=access_token,
            user=UserOut(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                role=user.role,
                is_active=user.is_active,
                xp=user.xp,
            )
        )
        
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Вход в систему",
    description="Аутентифицирует пользователя и возвращает JWT токен"
)
async def login(
    data: UserLoginIn,
    session: AsyncSession = Depends(get_db_session),
) -> TokenResponse:
    """Вход в систему"""
    
    # Получаем пользователя по email
    user = await user_repo.get_user_by_email(session, data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Проверяем пароль
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Проверяем, что пользователь активен
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Создаем токен
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return TokenResponse(
        access_token=access_token,
        user=UserOut(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            xp=user.xp,
        )
    )


@router.get(
    "/me",
    response_model=UserOut,
    summary="Получить текущего пользователя",
    description="Возвращает информацию о текущем аутентифицированном пользователе"
)
async def get_current_user_info(
    current_user: CurrentUserDep,
) -> UserOut:
    """Получить информацию о текущем пользователе"""
    return UserOut(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        is_active=current_user.is_active,
        xp=current_user.xp,
    )


@router.get(
    "/me/rating-percentile",
    response_model=RatingPercentileResponse,
    summary="Получить процентиль рейтинга",
    description="Возвращает процент пользователей с более низким рейтингом CV"
)
async def get_user_rating_percentile(
    current_user: CurrentUserDep,
    session: AsyncSession = Depends(get_db_session),
) -> RatingPercentileResponse:
    """Получить процентиль рейтинга пользователя"""
    
    percentile = await user_repo.get_user_rating_percentile(session, current_user.id)
    
    return RatingPercentileResponse(percentile=percentile)


@router.get(
    "/me/xp",
    response_model=UserXPResponse,
    summary="Получить информацию о XP",
    description="Возвращает детальную информацию о заработанном XP пользователя"
)
async def get_user_xp_info(
    current_user: CurrentUserDep,
    session: AsyncSession = Depends(get_db_session),
) -> UserXPResponse:
    """Получить информацию о XP пользователя"""
    
    # Получаем текущий XP пользователя
    current_xp = await user_repo.get_user_xp(session, current_user.id)
    
    # Получаем XP от бейджей
    from src.modules.badges import service as badge_service
    badge_stats = await badge_service.badge_service.get_user_badge_stats(session, current_user.id)
    xp_from_badges = badge_stats.total_xp_from_badges
    
    # Рассчитываем XP от активностей (всё остальное)
    xp_from_activities = max(0, current_xp - xp_from_badges)
    
    return UserXPResponse(
        current_xp=current_xp,
        xp_from_badges=xp_from_badges,
        xp_from_activities=xp_from_activities,
        total_earned=current_xp
    )