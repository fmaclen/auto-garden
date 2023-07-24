migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("kfdwb3cuh3vbnge")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "whxbmrjl",
    "name": "pump_gpio_bcm_pin",
    "type": "number",
    "required": false,
    "unique": false,
    "options": {
      "min": 0,
      "max": null
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("kfdwb3cuh3vbnge")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "whxbmrjl",
    "name": "pump_gpio_bcm_pin",
    "type": "number",
    "required": true,
    "unique": false,
    "options": {
      "min": null,
      "max": null
    }
  }))

  return dao.saveCollection(collection)
})
