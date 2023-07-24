migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("kfdwb3cuh3vbnge")

  // remove
  collection.schema.removeField("f4lmxcoc")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "vtb64nur",
    "name": "device",
    "type": "relation",
    "required": false,
    "unique": false,
    "options": {
      "collectionId": "8gfvyih1w3lb3c7",
      "cascadeDelete": false,
      "minSelect": null,
      "maxSelect": 1,
      "displayFields": []
    }
  }))

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "k42mjirc",
    "name": "moisture_sensor_dry",
    "type": "number",
    "required": true,
    "unique": false,
    "options": {
      "min": null,
      "max": null
    }
  }))

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "4zlbd5wx",
    "name": "moisture_sensor_wet",
    "type": "number",
    "required": true,
    "unique": false,
    "options": {
      "min": null,
      "max": null
    }
  }))

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "zgywkaed",
    "name": "moisture_sensor_pin",
    "type": "number",
    "required": false,
    "unique": false,
    "options": {
      "min": 0,
      "max": null
    }
  }))

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "whxbmrjl",
    "name": "pump_relay_pin",
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

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "f4lmxcoc",
    "name": "irrigation_frequency_in_s",
    "type": "number",
    "required": true,
    "unique": false,
    "options": {
      "min": null,
      "max": null
    }
  }))

  // remove
  collection.schema.removeField("vtb64nur")

  // remove
  collection.schema.removeField("k42mjirc")

  // remove
  collection.schema.removeField("4zlbd5wx")

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
})
