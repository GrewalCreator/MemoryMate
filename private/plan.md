# This is the database schema

## MongoDB

- users
  - Id (auto gen)
  - Name
  - birthdate
  - verifiied date
  - People: [{
    - name
    - description
    - images = []
      }]
  - Places: [{
    - description
    - image: url
      }]

## Cloudnary

- Images - URL(stored in mongo db)
