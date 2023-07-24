migrate((db) => {
  const snapshot = [
    {
      "id": "kfdwb3cuh3vbnge",
      "created": "2023-07-02 15:47:56.909Z",
      "updated": "2023-07-07 12:42:57.403Z",
      "name": "pots",
      "type": "base",
      "system": false,
      "schema": [
        {
          "system": false,
          "id": "0ylmrrcl",
          "name": "name",
          "type": "text",
          "required": false,
          "unique": false,
          "options": {
            "min": null,
            "max": null,
            "pattern": ""
          }
        },
        {
          "system": false,
          "id": "rgrsvbco",
          "name": "moisture_low",
          "type": "number",
          "required": false,
          "unique": false,
          "options": {
            "min": null,
            "max": null
          }
        },
        {
          "system": false,
          "id": "5v83jwrh",
          "name": "moisture_high",
          "type": "number",
          "required": true,
          "unique": false,
          "options": {
            "min": null,
            "max": null
          }
        },
        {
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
        },
        {
          "system": false,
          "id": "gla3vlbk",
          "name": "pump_max_attempts",
          "type": "number",
          "required": true,
          "unique": false,
          "options": {
            "min": 1,
            "max": null
          }
        },
        {
          "system": false,
          "id": "pfpkuavf",
          "name": "pump_frequency_in_s",
          "type": "number",
          "required": true,
          "unique": false,
          "options": {
            "min": null,
            "max": null
          }
        },
        {
          "system": false,
          "id": "79ajwih7",
          "name": "pump_duration_in_s",
          "type": "number",
          "required": true,
          "unique": false,
          "options": {
            "min": null,
            "max": null
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
    },
    {
      "id": "93vdgukzmtyoi3e",
      "created": "2023-07-02 15:48:09.613Z",
      "updated": "2023-07-07 12:39:28.679Z",
      "name": "moistures",
      "type": "base",
      "system": false,
      "schema": [
        {
          "system": false,
          "id": "l64hkauf",
          "name": "level",
          "type": "number",
          "required": false,
          "unique": false,
          "options": {
            "min": null,
            "max": null
          }
        },
        {
          "system": false,
          "id": "8xmfohz7",
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
        }
      ],
      "indexes": [],
      "listRule": null,
      "viewRule": null,
      "createRule": null,
      "updateRule": null,
      "deleteRule": null,
      "options": {}
    },
    {
      "id": "mqbo58z8cyqfof8",
      "created": "2023-07-02 15:49:36.890Z",
      "updated": "2023-07-07 12:39:28.673Z",
      "name": "irrigations",
      "type": "base",
      "system": false,
      "schema": [
        {
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
        },
        {
          "system": false,
          "id": "ufn1oowg",
          "name": "status",
          "type": "select",
          "required": false,
          "unique": false,
          "options": {
            "maxSelect": 1,
            "values": [
              "success",
              "error",
              "in_progress"
            ]
          }
        },
        {
          "system": false,
          "id": "iw1vjtk7",
          "name": "pumps",
          "type": "number",
          "required": false,
          "unique": false,
          "options": {
            "min": null,
            "max": null
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
    }
  ];

  const collections = snapshot.map((item) => new Collection(item));

  return Dao(db).importCollections(collections, true, null);
}, (db) => {
  return null;
})
