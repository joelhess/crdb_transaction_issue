from db import db, cockroach_transaction
from organizations_models import Organization


def main():
    db = setup_db()

    # Create the first Org Record
    organization1 = create_organization()   
    # Create a second Org Record with the same name to bump into the unique constraint
    organization2 = create_organization()   



@cockroach_transaction
def create_organization(db_session):
    organization = Organization(name="Test Org", label="Test Org Label")
    db_session.add(organization)
    db_session.flush()
    db_session.refresh(organization)
    return organization
    

def setup_db():
    db.init_connection()
    db.create_database()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        raise e
