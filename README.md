# LangChain & LangGraph Learning Lab

A notebook-first learning repository for LLM application fundamentals: model calls, prompts, structured output, LangChain chains, tool-using agents, and stateful LangGraph workflows. The notebooks use gpt-4o-mini through OpenRouter's OpenAI-compatible API.

## Purpose

An LLM generates text, but a useful AI application also needs reusable instructions, reliable data shapes, external capabilities, memory, and clear control over what happens next. This repository studies those layers in a practical sequence.

~~~text
Chat model
  -> prompts and messages
  -> structured output
  -> LangChain runnables and chains
  -> tools and ReAct agents
  -> LangGraph state, nodes, edges, loops, and human approval
~~~

| Component | Role in this repository |
| --- | --- |
| LangChain | Application building blocks: chat models, prompts, messages, output parsers, runnables, tools, and agents. |
| LangGraph | Orchestration: nodes update shared state and edges decide which node runs next. |
| Pydantic and TypedDict | Data contracts for model responses and graph state. |
| OpenRouter | The OpenAI-compatible model gateway configured through ChatOpenAI. |

## Architecture

All examples call ChatOpenAI, which sends model requests to OpenRouter. This provider boundary means prompts, graph logic, chains, and tools can remain unchanged if the model provider changes.

~~~text
Prompt / messages --+
Schema            --+--> ChatOpenAI --> OpenRouter --> model
Tool / runnable   --+
                     |
                     +--> StateGraph: state -> node -> updated state -> edge -> next node
~~~

A LangGraph node is ordinary Python code. It reads state, runs deterministic logic or calls an LLM/tool, and returns updated state fields. Edges define valid transitions. Conditional edges inspect state and select a branch. Compiling a graph turns this definition into an invokable workflow.

## What each section contains

### Langchain/Tutorial

| Notebook | Concepts demonstrated |
| --- | --- |
| LLM_Call.ipynb | The same chat request through the OpenAI SDK, ChatOpenAI, and init_chat_model. |
| Messages.ipynb | HumanMessage, SystemMessage, PromptTemplate, and ChatPromptTemplate. |
| Structured_Output.ipynb | Prompt-formatted output compared with Pydantic and TypedDict structured output. |

A prompt template is a reusable instruction with variables such as topic. Messages make a conversation explicit: a system message sets behavior, a human message supplies the request, an AI message contains a model response, and a tool message carries a tool result back to the model.

Structured output turns ambiguous natural language into predictable data. Pydantic validates fields at runtime, supports field descriptions, and gives typed attribute access. TypedDict documents a dictionary shape and is lightweight for graph state, but does not itself validate values at runtime. Calling with_structured_output with a schema makes the schema part of the model contract.

### Langchain/Chains

| Notebook | Concepts demonstrated |
| --- | --- |
| First_Chain.ipynb | Prompt -> model -> StrOutputParser, invoked manually and through LCEL and RunnableSequence. |
| CustomRunnable_Chain.ipynb | RunnableLambda changes intermediate text into the dictionary shape expected by the next prompt. |
| Parallel_Chain.ipynb | RunnableParallel produces LinkedIn and Instagram content from one movie summary. |
| Conditional_Chain.ipynb | A structured Positive/Negative classification selects a content-generation branch with RunnableBranch. |

LCEL, LangChain Expression Language, uses the pipe operator to compose compatible runnables.

~~~text
input -> prompt template -> chat model -> output parser -> next runnable
~~~

This is a data pipeline, not just shorthand. Every stage has a clear input/output shape. StrOutputParser extracts plain text, RunnableLambda runs normal Python transformations, RunnableParallel fans out independent work, and RunnableBranch makes a data-driven choice between downstream paths.

### Langchain/ReACT

| File | Concepts demonstrated |
| --- | --- |
| Intro.ipynb | A create_agent ReAct agent using DuckDuckGo, Wikipedia, and a custom enterprise-search tool; agent event streaming. |
| DB_Agent.ipynb | SQLDatabase and SQLDatabaseToolkit exposed to an agent for the local SQLite sales database. |
| init_db.py | Creation and population of the sample sales table. |
| demo.py | Direct inspection of the SQLite rows. |

A tool is a callable capability described to a model by name, description, and argument schema. The model proposes a tool call; application code executes it and returns an observation. The model does not execute Python directly.

ReAct means Reason plus Act. An agent decides what information it needs, calls a suitable tool, observes the result, and either acts again or produces an answer. The database agent applies this approach to SQL by exposing database-aware tools rather than relying on one hard-coded query.

### LangGraph/Foundation

| Notebook | Concepts demonstrated |
| --- | --- |
| FirstGraph.ipynb | TypedDict state, a welcome node, START/END, compilation, visualization, and invocation. |
| Messages.ipynb | Manual message-list updates versus an Annotated List add reducer. |
| Prompts.ipynb | ChatPromptTemplate construction and composition with a chat model. |
| Pydantic.ipynb | Pydantic graph state, model_dump updates, and model_validate revalidation. |

LangGraph carries shared state through a directed workflow. State may hold user input, messages, routing decisions, drafts, feedback, tasks, results, and counters. A reducer specifies how updates merge. The message reducer in this project appends messages rather than replacing the existing list; reducers are crucial when more than one branch may update a field.

### LangGraph/Workflow_Patterns

| Notebook | Pattern and implementation |
| --- | --- |
| Router.ipynb | Structured output selects Instagram, Twitter, or LinkedIn; a conditional edge routes to that post node. |
| Parallelization.ipynb | Three generation nodes start from START and write independent fields in shared state. |
| Generator_Evaluator.ipynb | A joke is generated, evaluated, improved from feedback, and limited to three iterations. |
| Orchestrator_Worker.ipynb | An orchestrator creates tasks, workers execute them concurrently, and a collector summarizes results. |

~~~text
Sequential:      START -> A -> B -> END
Routing:         START -> classify -> selected node -> END
Parallel:        START -> Instagram / Twitter / LinkedIn -> END
Evaluation loop: START -> generate -> evaluate -> retry or END
Orchestration:   request -> plan -> parallel workers -> collector -> END
~~~

The router separates probabilistic work from deterministic work: the LLM produces a constrained classification, then Python maps it to a valid graph edge. The generator-evaluator example demonstrates bounded feedback loops. Its max_iterations counter guarantees the workflow eventually stops. The orchestrator-worker example shows task decomposition, concurrent execution through ThreadPoolExecutor, and result aggregation. Production systems should limit concurrency for API cost and rate-limit safety.

### LangGraph/Agents_and_Runtime

| Notebook | Concepts demonstrated |
| --- | --- |
| ToolBinding.ipynb | DuckDuckGo, arXiv, Wikipedia, and local personal_info tools bound to a model. |
| ReACT.ipynb | A manual tool loop with LLM and tool nodes, ToolMessage results, graph routing, and streaming. |
| HumanInLoop.ipynb | Approval interrupts, Command resume, thread IDs, and MemorySaver. |
| Memory.ipynb | Reserved for persistence; it currently duplicates FirstGraph.ipynb. |

The approval graph is a key safety pattern:

~~~text
START -> approval -> interrupt -> human decision
                                  -> approve -> proceed -> approved
                                  -> reject  -> cancel  -> rejected
~~~

interrupt pauses execution and returns structured details for a user interface. Command resume continues the same execution. A thread ID identifies it and a checkpointer retains its state. MemorySaver is appropriate for a notebook demonstration; production applications need durable shared persistence.

## Suggested study order

1. Langchain/Tutorial: model calls, message roles, templates, and schemas.
2. Langchain/Chains: serial, custom, parallel, and conditional composition.
3. Langchain/ReACT: tools, agents, and the SQL toolkit.
4. LangGraph/Foundation: state, nodes, edges, reducers, and validation.
5. LangGraph/Workflow_Patterns: router, parallelization, evaluator loop, then orchestration.
6. LangGraph/Agents_and_Runtime: tool loops, checkpoints, and human oversight.

## Data and safety boundaries

The notebooks use the OPENROUTER_API_KEY environment variable. The real .env is ignored by Git and .env.example documents the expected variable. Credentials must never be committed or left in notebook outputs.

Langchain/ReACT/SalesDB/sales.db is educational sample data. A production SQL agent should use read-only credentials, table and operation allowlists, query limits, audit logs, and human review before any mutating action.

## Current implementation notes

- Agents_and_Runtime/Memory.ipynb currently duplicates FirstGraph.ipynb. Replace it with a checkpointed multi-turn conversation or thread-memory example.
- A second HumanInLoop.ipynb exists at the LangGraph root. Keep the Agents_and_Runtime version as the canonical lesson after committing the reorganization.
- The custom ReACT graph has the right learning components, but its post-LLM route should check whether the latest AIMessage has tool_calls. Checking for a ToolMessage immediately after an LLM node can end the graph before tool execution.
- Review or clear notebook outputs before publishing, especially if they include private prompts, data, or API responses.

## Scope

The purpose of this repository is to develop sound intuition for agentic systems: explicit data contracts, composable transformations, controlled tools, stateful execution, bounded loops, and human oversight. The next evolution would be a tested Python package with reusable state models, configuration, tracing, durable storage, and evaluation cases.
