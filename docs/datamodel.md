# Data model

```json
{
    "center": <entity_id>,
    "entities" [
        <list of entities>
    ],
    "relationships": [
        <list of relationships>
    ],
    "relationship_types": [
        <list of relationship_types>
    ]
}

```

where an entity is as follows:

```json
{
    "id": <something unique>,
    "aliases": [<list of strings>], // optional
    "notes": <string>, // optional
}
```

and a relationship_type is as follows:

```json
{
    "id": <something unique>,
    "icon": <string of emojis>,
    "description": <string>
    "oriented": <boolean> // optional, default false
}
```
and a relationship is as follows:
```json
{
    "id_left": <entity_id>,
    "id_right": <entity_id>,
    "id_relationship_type": <relationship_type_id>,
}
```

# Full example

See `matcha.json`