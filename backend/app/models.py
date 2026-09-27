"""Sprint 1 data model – mirrors docs/diagrams/erd.puml (draft, refined in Sprint 2)."""
import enum
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Role(str, enum.Enum):
    MARKETING = "Marketing"
    PROD_MANAGER = "ProdManager"
    PRODEE = "Prodee"
    PO = "PO"
    FLOOR_MANAGER = "FloorManager"
    STAMPER = "Stamper"


class MachineStatus(str, enum.Enum):
    AVAILABLE = "available"
    RUNNING = "running"
    MAINTENANCE = "maintenance"
    FAULT = "fault"


class DocType(str, enum.Enum):
    DRAWING = "drawing"
    SPECIFICATION = "specification"
    INSTRUCTION = "instruction"


class BatchStatus(str, enum.Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    HALTED = "halted"
    DONE = "done"


# ---------- People & plant ----------
class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    role: Mapped[Role] = mapped_column(Enum(Role))
    password_hash: Mapped[str] = mapped_column(String(255), default="")
    certifications: Mapped[list["Certification"]] = relationship(back_populates="stamper")


class MachineType(Base):
    __tablename__ = "machine_types"
    type_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)


class Machine(Base):
    __tablename__ = "machines"
    machine_id: Mapped[int] = mapped_column(primary_key=True)
    type_id: Mapped[int] = mapped_column(ForeignKey("machine_types.type_id"))
    model: Mapped[str] = mapped_column(String(80))
    max_capacity_per_hour: Mapped[int] = mapped_column(Integer)
    status: Mapped[MachineStatus] = mapped_column(Enum(MachineStatus), default=MachineStatus.AVAILABLE)
    machine_type: Mapped[MachineType] = relationship()


class Certification(Base):
    __tablename__ = "certifications"
    cert_id: Mapped[int] = mapped_column(primary_key=True)
    stamper_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    type_id: Mapped[int] = mapped_column(ForeignKey("machine_types.type_id"))
    issued_on: Mapped[date] = mapped_column(Date)
    expires_on: Mapped[date | None] = mapped_column(Date, nullable=True)
    stamper: Mapped[User] = relationship(back_populates="certifications")
    machine_type: Mapped[MachineType] = relationship()


# ---------- Product lifecycle ----------
class ProductLine(Base):
    __tablename__ = "product_lines"
    line_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)


class Product(Base):
    __tablename__ = "products"
    product_id: Mapped[int] = mapped_column(primary_key=True)
    line_id: Mapped[int] = mapped_column(ForeignKey("product_lines.line_id"))
    name: Mapped[str] = mapped_column(String(80))
    version: Mapped[str] = mapped_column(String(20), default="1.0")


class DesignDocument(Base):
    __tablename__ = "design_documents"
    doc_id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"))
    doc_type: Mapped[DocType] = mapped_column(Enum(DocType))
    file_url: Mapped[str] = mapped_column(String(255))
    uploaded_by: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    version: Mapped[str] = mapped_column(String(20), default="1.0")


# ---------- Materials & procurement ----------
class Material(Base):
    __tablename__ = "materials"
    material_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    unit: Mapped[str] = mapped_column(String(20))
    stock_qty: Mapped[float] = mapped_column(Float, default=0)
    reorder_level: Mapped[float] = mapped_column(Float, default=0)


class BillOfMaterial(Base):
    __tablename__ = "bill_of_materials"
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"), primary_key=True)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.material_id"), primary_key=True)
    qty_per_unit: Mapped[float] = mapped_column(Float)


class Supplier(Base):
    __tablename__ = "suppliers"
    supplier_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    contact: Mapped[str] = mapped_column(String(120), default="")
    lead_time_days: Mapped[int] = mapped_column(Integer, default=7)


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    po_id: Mapped[int] = mapped_column(primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.supplier_id"))
    raised_by: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    status: Mapped[str] = mapped_column(String(20), default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PurchaseOrderLine(Base):
    __tablename__ = "purchase_order_lines"
    po_id: Mapped[int] = mapped_column(ForeignKey("purchase_orders.po_id"), primary_key=True)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.material_id"), primary_key=True)
    qty: Mapped[float] = mapped_column(Float)
    unit_price: Mapped[float] = mapped_column(Float, default=0)


# ---------- Orders & production ----------
class CustomerOrder(Base):
    __tablename__ = "customer_orders"
    order_id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(100))
    due_date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), default="received")


class OrderItem(Base):
    __tablename__ = "order_items"
    item_id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("customer_orders.order_id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"))
    qty: Mapped[int] = mapped_column(Integer)
    colour: Mapped[str] = mapped_column(String(40), default="")
    size: Mapped[str] = mapped_column(String(20), default="")
    lid_handle_material: Mapped[str] = mapped_column(String(40), default="")
    signature_text: Mapped[str] = mapped_column(String(60), default="")


class ProductionBatch(Base):
    __tablename__ = "production_batches"
    batch_id: Mapped[int] = mapped_column(primary_key=True)
    order_item_id: Mapped[int] = mapped_column(ForeignKey("order_items.item_id"))
    status: Mapped[BatchStatus] = mapped_column(Enum(BatchStatus), default=BatchStatus.PLANNED)


class JobSheet(Base):
    __tablename__ = "job_sheets"
    sheet_id: Mapped[int] = mapped_column(primary_key=True)
    stamper_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    shift_date: Mapped[date] = mapped_column(Date)
    shift_no: Mapped[int] = mapped_column(Integer)  # 1 or 2 (two 8-hour shifts)
    prepared_by: Mapped[int] = mapped_column(ForeignKey("users.user_id"))


class JobCard(Base):
    __tablename__ = "job_cards"
    job_id: Mapped[int] = mapped_column(primary_key=True)
    sheet_id: Mapped[int] = mapped_column(ForeignKey("job_sheets.sheet_id"))
    batch_id: Mapped[int] = mapped_column(ForeignKey("production_batches.batch_id"))
    machine_id: Mapped[int] = mapped_column(ForeignKey("machines.machine_id"))
    design_doc_id: Mapped[int | None] = mapped_column(ForeignKey("design_documents.doc_id"), nullable=True)
    task: Mapped[str] = mapped_column(String(120))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(20), default="scheduled")


class MachineReading(Base):
    __tablename__ = "machine_readings"
    reading_id: Mapped[int] = mapped_column(primary_key=True)
    machine_id: Mapped[int] = mapped_column(ForeignKey("machines.machine_id"))
    job_id: Mapped[int | None] = mapped_column(ForeignKey("job_cards.job_id"), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    cycle_speed: Mapped[float] = mapped_column(Float, default=0)
    output_count: Mapped[int] = mapped_column(Integer, default=0)
    fault_code: Mapped[str | None] = mapped_column(String(20), nullable=True)


class QualityCheck(Base):
    __tablename__ = "quality_checks"
    qc_id: Mapped[int] = mapped_column(primary_key=True)
    batch_id: Mapped[int] = mapped_column(ForeignKey("production_batches.batch_id"))
    checked_by: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    result: Mapped[str] = mapped_column(String(10))  # pass / fail
    notes: Mapped[str] = mapped_column(Text, default="")


class Notification(Base):
    __tablename__ = "notifications"
    notif_id: Mapped[int] = mapped_column(primary_key=True)
    recipient_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    type: Mapped[str] = mapped_column(String(30))
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
