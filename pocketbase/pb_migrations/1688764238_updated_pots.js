migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("kfdwb3cuh3vbnge")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "zgywkaed",
    "name": "moisture_sensor_ads_channel",
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
    "id": "zgywkaed",
    "name": "moisture_sensor_ads_channel",
    "type": "number",
    "required": true,
    "unique": false,
    "options": {
      "min": 0,
      "max": null
    }
  }))

  return dao.saveCollection(collection)
})
