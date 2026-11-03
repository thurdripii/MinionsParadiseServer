
# MinionsParadiseBrazil API

Version: 0.2.0-dev

Status: Experimental

Base URL:
http://localhost:8000

## Server

### GET /

Returns basic server information.

### GET /health

Checks server and database status.

### GET /ready

Checks basic server availability.

### GET /config

Returns server configuration and enabled features.

## Accounts

### POST /rest/user/register

Creates an anonymous player.

Success response: HTTP 201.

### GET /rest/user/{player_id}

Returns player information.

## Sessions

### POST /rest/user/session

Creates a player session.

Request body:

{
  "userId": "PLAYER_ID"
}

### POST /rest/user/session/validate

Validates a session.

Request body:

{
  "userId": "PLAYER_ID",
  "sessionKey": "SESSION_KEY"
}

## GameState

Both endpoints require:

User-Id: PLAYER_ID
Session-Key: SESSION_KEY

### GET /rest/gamestate/{player_id}

Retrieves saved player progress.

### POST /rest/gamestate/{player_id}

Saves player progress.

Request body:

A JSON object containing the game state.

Maximum size: 1 MB.

## Compatibility

This API is experimental.

Compatibility with the original Minions Paradise
server protocol has not been confirmed.
