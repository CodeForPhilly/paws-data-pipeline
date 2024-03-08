# Dependabot PRs
- [Dependabot PRs](#dependabot-prs)
  - [Frontend Dependabot PRs](#frontend-dependabot-prs)
  - [Backend Dependabot PRs](#backend-dependabot-prs)

## Frontend Dependabot PRs
As the client facing part of the app is pretty minimal, this process should cover most frontend dependabot PRs.

- Pull dependabot PR
```
gh pr checkout [prNumber]
```

- Rebuild and run the container
```
docker-compose down -v
docker-compose build
docker-compose up
```

- Log into `base_admin` user
- Go to `Admin` page
  - Upload 2 Volgistics data CSVs in the same upload action
  - Click `Run Data Analysis`
- Go to `Users` page
  - Create new user
  - Update user via `Update User` button
  - Change user password via `Change Password` button
- Go to 360 Dataview
  - Search for a common name
  - Click the user to make sure page renders correctly
- Log out

If the package patch notes look non-breaking and you encounter no errors in this process, the Dependabot PR should be safe to merge.

## Backend Dependabot PRs
Documentation needed.
