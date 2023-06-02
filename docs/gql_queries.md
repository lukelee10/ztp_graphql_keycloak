Copy and paste the following queries into the GraphQL Playground to test them out.

## Search Cells

```groovy
query SearchOPAQuery {
  currentUser {
    username
    clearance {
      name
    }
    accessAttributes {
      name
    }
  }
  searchOpa(searchTerm: "") {
    __typename
    classification {
      name
    }
    accessAttributes {
      name
    }
    row {
      id
      classification {
        name
      }
      accessAttributes {
        name
      }
    }
    column {
      name
      classification {
        name
      }
      accessAttributes {
        name
      }
    }
    data
  }
}
```

## Get a specific table

```groovy
query GetTableQuery($tableId: Int!) {
  getTable(tableId: $tableId) {
    id
    name
    accessAttributes {
      id
      name
    }
    classification {
      id
      name
    }
    columns {
      accessAttributes {
        id
        name
      }
      classification {
        id
        name
      }
      id
      name
    }
    rows {
      id
      accessAttributes {
        id
        name
      }
      classification {
        id
        name
      }
      cells {
        accessAttributes {
          id
          name
        }
        classification {
          id
          name
        }
        data
      }
    }
  }
}
```
