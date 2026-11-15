from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Numeric, DateTime, func
from decimal import Decimal
from datetime import datetime



class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(50))
    statistic: Mapped["StatisticModel"] = relationship(back_populates="owner", cascade="all, delete-orphan", uselist=False)
    games: Mapped[list["GameStatModel"]] = relationship(back_populates="player", cascade="all, delete-orphan")

class StatisticModel(Base):
    __tablename__ = "statistics"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    owner: Mapped["UserModel"] = relationship(back_populates="statistic")

    total_hs: Mapped[int] = mapped_column(default=0)
    total_wins: Mapped[int] = mapped_column(default=0)
    total_loses: Mapped[int] = mapped_column(default=0)
    total_kills: Mapped[int] = mapped_column(default=0)
    total_deaths: Mapped[int] = mapped_column(default=0)
    total_assists: Mapped[int] = mapped_column(default=0)
    total_games: Mapped[int] = mapped_column(default=0)

    @property
    def total_win_rate(self) -> float:
        if self.total_games == 0:
            return 0.0
        return round((self.total_wins / self.total_games) * 100, 2)
    
    @property
    def total_kd_rate(self) -> float:
        if self.total_deaths == 0:
            return float(self.total_kills)
        return round(self.total_kills / self.total_deaths, 2)


class GameStatModel(Base):
    __tablename__ = "game_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    player: Mapped["UserModel"] = relationship(back_populates="games")

    played_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    duration_seconds: Mapped[int] = mapped_column()
    outcome: Mapped[bool] = mapped_column()
    hs_rate: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    hs_count: Mapped[int] = mapped_column()
    kills: Mapped[int] = mapped_column()
    deaths: Mapped[int] = mapped_column()
    assists: Mapped[int] = mapped_column()
    kd_rate: Mapped[Decimal] = mapped_column(Numeric(5, 2))

    def format_duration(seconds: int) -> str:
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)

        if hours > 0:
            return f"{hours}h {minutes}min {secs}s"
        return f"{minutes}min {seconds}s"