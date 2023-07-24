migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("mqbo58z8cyqfof8")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "1hvncyoz",
    "name": "pot",
    "type": "relation",
    "required": false,
    "unique": false,
    "options": {
      "collectionId": "kfdwb3cuh3vbnge",
      "cascadeDelete": true,
      "minSelect": null,
      "maxSelect": 1,
      "displayFields": []
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("mqbo58z8cyqfof8")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "1hvncyoz",
    "name": "pot",
    "type": "relation",
    "required": false,
    "unique": false,
    "options": {
      "collectionId": "kfdwb3cuh3vbnge",
      "cascadeDelete": false,
      "minSelect": null,
      "maxSelect": 1,
      "displayFields": []
    }
  }))

  return dao.saveCollection(collection)
})
