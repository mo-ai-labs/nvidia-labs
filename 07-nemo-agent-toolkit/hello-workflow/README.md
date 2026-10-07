# NeMo Agent Toolkit: hello workflow (NCP-AAI W02 D03)

## §1 Bet

**Bet A:** I ask the NAT agent to flag alert A-1001, but `flag_alert` isn't in its `include` allowlist. My guess: **Refuses / says it can't**.

## §2 NAT in one paragraph

NAT wraps agents built in other frameworks (LangGraph, ADK, plain Python) instead of replacing them, so it is not a LangGraph replacement.
On my ADK platform it would add profiling, evaluation, observability and config-driven composition (swap model/tools from YAML) without a rewrite.

## §3 Config walkthrough

NAT ran the ReAct loop for me (prompting, parsing Thought/Action, retries), which I wrote by hand on Day 2.
It started the stdio MCP server from YAML and acted as the MCP client that discovers the tools, which my Day 5 bridge did by hand.
It wired the NIM model and the tool list from config instead of in code.
Gotcha: NAT's NIM default `max_tokens` is 300, so a reasoning model's thoughts got cut off and the ReAct parser failed; `max_tokens: 4096` fixed it.

## §4 Allowlist test

Without `flag_alert` in `include`, the agent made no tool call and its final answer just echoed my request as if it was done (the bet was a loss: I guessed it would refuse). With it, the agent called `fincrime__flag_alert` and answered from the server's reply.
A server-side allowlist is the stronger control because it blocks the tool for every client of that server; a client-side `include` only narrows one agent.
I want both: defence in depth, per-agent narrowing of a shared server, and protection against other clients of the same server.
