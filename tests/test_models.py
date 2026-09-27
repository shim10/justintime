from datetime import date

from app import models as m


def test_all_erd_entities_have_tables(db):
    expected = {"users", "machine_types", "machines", "certifications", "product_lines", "products",
                "design_documents", "materials", "bill_of_materials", "suppliers", "purchase_orders",
                "purchase_order_lines", "customer_orders", "order_items", "production_batches",
                "job_sheets", "job_cards", "machine_readings", "quality_checks", "notifications"}
    assert expected <= set(m.Base.metadata.tables)


def test_stamper_can_hold_multiple_certifications(db):
    stamping = m.MachineType(name="stamping")
    coating = m.MachineType(name="coating")
    mattie = m.User(name="Mattie Float", email="mattie@floatfry.test", role=m.Role.STAMPER)
    db.add_all([stamping, coating, mattie])
    db.flush()
    db.add_all([
        m.Certification(stamper_id=mattie.user_id, type_id=stamping.type_id, issued_on=date(2020, 1, 1)),
        m.Certification(stamper_id=mattie.user_id, type_id=coating.type_id, issued_on=date(2021, 6, 1)),
    ])
    db.commit()
    assert {c.machine_type.name for c in mattie.certifications} == {"stamping", "coating"}


def test_order_item_stores_customisation(db):
    line = m.ProductLine(name="Rosemary TS1")
    db.add(line)
    db.flush()
    prod = m.Product(line_id=line.line_id, name="Rosemary TS1 Saucepan")
    order = m.CustomerOrder(customer_name="Test Customer", due_date=date(2026, 11, 1))
    db.add_all([prod, order])
    db.flush()
    item = m.OrderItem(order_id=order.order_id, product_id=prod.product_id, qty=2, colour="Sage",
                       size="20cm", lid_handle_material="Walnut", signature_text="The Floats")
    db.add(item)
    db.commit()
    assert db.get(m.OrderItem, item.item_id).signature_text == "The Floats"
