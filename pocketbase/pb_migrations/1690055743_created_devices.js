migrate((db) => {
  const collection = new Collection({
    "id": "8gfvyih1w3lb3c7",
    "created": "2023-07-22 19:55:43.963Z",
    "updated": "2023-07-22 19:55:43.963Z",
    "name": "devices",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "ywykxhab",
        "name": "name",
        "type": "text",
        "required": true,
        "unique": false,
        "options": {
          "min": null,
          "max": null,
          "pattern": ""
        }
      }
    ],
    "indexes": [],
    "listRule": null,
    "viewRule": null,
    "createRule": null,
    "updateRule": null,
    "deleteRule": null,
    "options": {}
  });

  return Dao(db).saveCollection(collection);
}, (db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("8gfvyih1w3lb3c7");

  return dao.deleteCollection(collection);
})
