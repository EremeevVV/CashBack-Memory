from datetime import datetime

import pytz
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Card(Base):
    __tablename__ = 'card'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    memo_number: Mapped[int] = mapped_column(nullable=False)
    bank_id: Mapped[int] = mapped_column(ForeignKey('bank.id', name='fk_card_bank'), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('owner.id', name='fk_card_owner'), nullable=False)

    bank: Mapped['Bank'] = relationship('Bank', back_populates='cards')
    owner: Mapped['Owner'] = relationship('Owner', back_populates='cards')


class Promotion(Base):
    __tablename__ = 'promotion'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    start_date: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now(tz=pytz.utc))
    end_date: Mapped[datetime | None] = mapped_column(nullable=True)
    percent: Mapped[float] = mapped_column(nullable=False)
    card_id: Mapped[int] = mapped_column(ForeignKey('card.id', name='fk_promotion_card'), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id', name='fk_promotion_category'), nullable=False)

    card: Mapped['Card'] = relationship('Card', back_populates='promotions')
    category: Mapped['Category'] = relationship('Category', back_populates='promotions')


class Bank(Base):
    __tablename__ = 'bank'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)

    cards: Mapped[list['Card']] = relationship('Card')


class Owner(Base):
    __tablename__ = 'owner'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)

    cards: Mapped[list['Card']] = relationship('Card')


class Category(Base):
    __tablename__ = 'category'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    special: Mapped[bool] = mapped_column(nullable=False)

    promotions: Mapped[list['Promotion']] = relationship('Promotion')
    mmcs: Mapped[list['MMC']] = relationship('MMC')


class MMC(Base):
    __tablename__ = 'mmc'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[int] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey(Category.id), nullable=False)

    category: Mapped['Category'] = relationship('Category', back_populates='mmcs')
    shops: Mapped[list['Shop']] = relationship('Shop')


class Shop(Base):
    __tablename__ = 'shop'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    mmc_id: Mapped[int] = mapped_column(ForeignKey(MMC.id), nullable=False)

    mmc: Mapped['MMC'] = relationship('MMC', back_populates='shops')
