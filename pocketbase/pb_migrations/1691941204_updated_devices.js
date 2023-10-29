migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("8gfvyih1w3lb3c7")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "etipjjde",
    "name": "ip",
    "type": "text",
    "required": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("8gfvyih1w3lb3c7")

  // remove
  collection.schema.removeField("etipjjde")

  return dao.saveCollection(collection)
})
