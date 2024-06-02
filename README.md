# Movie App

This is a simple movie application built with Flask, Flask-SQLAlchemy, and Graphene. It provides a GraphQL API for managing movies and genres.

## Features

- Fetch all genres and movies
- Fetch a specific genre or movie by ID
- Fetch movies associated with a specific genre
- Fetch the genre associated with a specific movie
- Create a new genre
- Update an existing genre
- Delete an existing genre

## Prerequisites

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Graphene

  2. Access the GraphQL API at `http://localhost:5000/graphql`.

## GraphQL Queries and Mutations

You can use tools like GraphiQL or Postman to interact with the GraphQL API. Here are some example queries and mutations:

### Queries

- Fetch all genres:

```graphql
query {
  genres {
    id
    name
  }
}

Fetch movies by genre ID:

graphqlCopy codequery {
  movies_by_genre(genre_id: 1) {
    id
    title
    description
    release_year
  }
}
Mutations

Create a new genre:

graphqlCopy codemutation {
  create_genre(name: "Action") {
    genre {
      id
      name
    }
  }
}

Update an existing genre:

graphqlCopy codemutation {
  update_genre(id: 1, name: "Comedy") {
    genre {
      id
      name
    }
  }
}
