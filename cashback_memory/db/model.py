from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Card(Base):
    __tablename__ = 'card'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    memo_number: Mapped[int] = mapped_column(nullable=False)
    bank_id: Mapped[int] = mapped_column(ForeignKey('bank.id', name='fk_card_bank'), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('owner.id', name='fk_card_owner'), nullable=False)

    bank: Mapped['Bank'] = relationship('Bank', back_populates='cards')
    owner: Mapped['Owner'] = relationship('Owner', back_populates='cards')
    promotions: Mapped[list['Promotion']] = relationship('Promotion')

    def __repr__(self) -> str:
        return (f"Card(id={self.id}, name='{self.name}', memo_number={self.memo_number},"
                f" bank_id={self.bank_id}, owner_id={self.owner_id})")


class Promotion(Base):
    __tablename__ = 'promotion'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    start_date: Mapped[date] = mapped_column(nullable=False, default=date.today)
    end_date: Mapped[date | None] = mapped_column(nullable=True)
    percent: Mapped[float] = mapped_column(nullable=False)
    card_id: Mapped[int] = mapped_column(ForeignKey('card.id', name='fk_promotion_card'), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id', name='fk_promotion_category'), nullable=False)

    card: Mapped['Card'] = relationship('Card', back_populates='promotions')
    category: Mapped['Category'] = relationship('Category', back_populates='promotions')

    def __repr__(self) -> str:
        return (f"Promotion(id={self.id}, start_date={self.start_date}, end_date={self.end_date}, "
                f"percent={self.percent}, card_id={self.card_id}, category_id={self.category_id})")


class Bank(Base):
    __tablename__ = 'bank'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    cards: Mapped[list['Card']] = relationship('Card')

    def __repr__(self) -> str:
        return f"Bank(id={self.id}, name='{self.name}')"


class Owner(Base):
    __tablename__ = 'owner'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    cards: Mapped[list['Card']] = relationship('Card')

    def __repr__(self) -> str:
        return f"Owner(id={self.id}, name='{self.name}')"


class Category(Base):
    __tablename__ = 'category'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    special: Mapped[bool] = mapped_column(default=False, nullable=False)

    promotions: Mapped[list['Promotion']] = relationship('Promotion')
    shops: Mapped[list['Shop']] = relationship('Shop')

    def __repr__(self) -> str:
        return f"Category(id={self.id}, name='{self.name}', description='{self.description}', special={self.special})"


class Shop(Base):
    __tablename__ = 'shop'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey(Category.id), nullable=False)

    category: Mapped['Category'] = relationship('Category', back_populates='shops')

    def __repr__(self) -> str:
        return f"Shop(id={self.id}, name='{self.name}', category_id={self.category_id})"
