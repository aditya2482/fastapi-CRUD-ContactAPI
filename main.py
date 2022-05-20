from fastapi import Body, FastAPI,Path
from pydantic import BaseModel, EmailStr
from typing import Optional

app = FastAPI()

contacts = {}
contacts_set=[] # changed to set - []

class Contact(BaseModel):
    name: str
    mobile: int
    email: EmailStr
    address: str
   
class UpdateContact(Contact):
    name: Optional[str] = None
    mobile: Optional[int] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
   
@app.post("/create-user/{contact_id}")
def createuser(contact_id: int, contact: Contact = Body(default={"name": "Acchint",
        "mobile": 1234567890,
        "email": "abc@example.com",
        "address": "Chittorgarh"})):
    if contact_id in contacts:
        return {"Error": "contact already exists"}
    else:
        if contact.mobile not in contacts_set:
            if not(str(contact.mobile).startswith("0")):
                if len(str(contact.mobile))==10: #checking if the mobile number already exists to reduce duplicacy - mobile numbers are unique
                    contacts[contact_id]= contact
                    contacts_set.append(contact.mobile)
                else:
                    return {"Error": "Contact number should be of 10 digits"}
            else:
                return {"Error": "Contact should not start with 0"}
        else:
            return {"Error": "contact already exists"}
    contacts[contact_id]= contact
    return contacts[contact_id]

@app.get("/get-user-byID/{contact_id}")
def getuserbyID(contact_id: int = Path(None, description = "Please Enter Id", gt = 0 )):
    if contact_id not in contacts:
        return {"Error": "contact does not exists"}
    return contacts[contact_id]

@app.patch("/update-user/{contact_id}")
def updateuser(contact_id: int, contact:UpdateContact):
    if contact_id not in contacts:
        return {"Error": "User does not exist"}
    if contact.name != None:
        contacts[contact_id].name=contact.name
        # contacts[contact_id]["name"]=contact.name
    if contact.mobile != None:
        contacts[contact_id].mobile=contact.mobile
        # contacts[contact_id]["mobile"]=contact.mobile
    if contact.email != None:
        contacts[contact_id].email=contact.email
        # contacts[contact_id]["email"]=contact.email
    if contact.address != None:
        contacts[contact_id].address=contact.address
        # contacts[contact_id]["address"]=contact.address
    # contacts[contact_id].update(dict1)
    return contacts[contact_id]

@app.delete("/delete-user/{contact_id}")
def deleteuser(contact_id: int):
    if contact_id not in contacts:
        return {"Error": "User does not exist"}
    del(contacts[contact_id])
    return {"msg": "user deleted"}