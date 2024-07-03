from fastapi import FastAPI
from prisma import Prisma
from schemas import PropertyCreate, PropertyUpdate
from fastapi.responses import RedirectResponse


prisma = Prisma()

async def lifespan(app: FastAPI):
    await prisma.connect()
    yield
    await prisma.disconnect()
    
    
app = FastAPI(lifespan=lifespan)

# Redirect "/" to "/docs"
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.post("/add_new_property/")
async def add_new_property(property: PropertyCreate):
    locality = await prisma.locality.find_first(where={"name": property.locality})
    if not locality:
        locality = await prisma.locality.create({"name": property.locality})
    new_property = await prisma.property.create({
        "property_name": property.property_name,
        "localityId": locality.id,
        "owner_name": property.owner_name,
    })
    return {"message": "Property added", "property_id": new_property.id}

@app.get("/fetch_all_properties/")
async def fetch_all_properties(locality_name: str):
    locality = await prisma.locality.find_first(where={"name": locality_name})
    if not locality:
        return []
    properties = await prisma.property.find_many(where={"localityId": locality.id})
    return properties

@app.put("/update_property_details/")
async def update_property_details(property: PropertyUpdate):
    updated_property = await prisma.property.update(data={"localityId": property.locality_id,"owner_name": property.owner_name,},where={"id": property.property_id})
    return {"message": "Property updated", "property": updated_property}

@app.delete("/delete_property_record/")
async def delete_property_record(property_id: str):
    await prisma.property.delete(where={"id": property_id})
    return {"message": "Property deleted"}
    