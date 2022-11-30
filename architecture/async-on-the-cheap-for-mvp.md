# Async on the cheap (for MVP)

### Introduction

It's recognized \[1, 2] that the best way to handle long-running tasks is to use a task queue, allowing separation of the middle layer (API server) and the execution server. But as we're trying to get an MVP out for feedback, it's not unreasonable to use a less-than-perfect solution for the interim. Here's a few ideas for discussion:

### _Continue to treat execute() as synchronous but stream back status information_

We've been operating (at the API server) with a model of _receive request, do work, return() with data_. But both Flask and JS support streaming data in chunks from server to client:\
Flask: [Streaming Contents](https://flask.palletsprojects.com/en/1.1.x/patterns/streaming/)\
JS: [Using readable streams](https://developer.mozilla.org/en-US/docs/Web/API/Streams\_API/Using\_readable\_streams)\
\
From the Flask side, the data it streams back would be status updates (_e.g._, every 100 rows processed) which the React client would use to update the display. When the server sends back "complete", React displays a nice completion message and the user proceeds to the 360 view.

#### **Evaluation**

Doesn't appear to require much heavy lifting at server or client (we would need to figure out how to feed the generator on the server) but may be a bit brittle; if there's any kind of network hiccup (or user reloads the page?) the stream would be broken and we wouldn't be able to tell the user anything useful.

### _Client aborts Fetch, polls status API until completion_

In this idea, instead of waiting for the execute() Fetch to complete, the React client uses an [AbortController](https://developer.mozilla.org/en-US/docs/Web/API/AbortController/abort) to cancel the pending Fetch. It then starts polling the API execution status endpoint, displaying updates until that endpoint reports that the operation is complete.

**Evaluation**

Using SQLAlchemy's `engine.dispose()`, and two uWSGI processes. I've got `/api/get_execution_status/<job_id>` working correctly. I'd probably want to have it find the latest job

![](https://user-images.githubusercontent.com/11001850/112061042-4ceb9580-8b34-11eb-8dc7-fb9eede44d7d.png)

instead of having to specify it (although we could use the streaming model above to send back the job\_id). We need to figure what side-effects there might be to cancelling the fetch. I presume the browser would drop the connection; will Flask assume it can kill the request?\
The client could check status when the page loads to see if there's a running job so it would be more robust in the face of network issues or reloads.

\[1] [https://flask.palletsprojects.com/en/1.1.x/patterns/celery/](https://flask.palletsprojects.com/en/1.1.x/patterns/celery/)\
\[2] [https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxii-background-jobs](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxii-background-jobs)

