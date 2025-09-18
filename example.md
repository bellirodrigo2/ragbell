---
title: Full-text search
description: Full-text search, also known as lexical search, is a technique for fast, efficient searching through text fields in documents. Documents and search queries...
url: https://www.elastic.co/docs/solutions/search/full-text
products:
  - Elasticsearch
---

# Full-text search

<tip>
  Would you prefer to start with a hands-on example? Refer to our [full-text search tutorial](https://www.elastic.co/docs/reference/query-languages/query-dsl/full-text-filter-tutorial).
</tip>

Full-text search, also known as lexical search, is a technique for fast, efficient searching through text fields in documents. Documents and search queries are transformed to enable returning [relevant](https://www.elastic.co/what-is/search-relevance) results instead of simply exact term matches. Fields of type [`text`](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/text#text-field-type) are analyzed and indexed for full-text search.
Built on decades of information retrieval research, full-text search delivers reliable results that scale predictably as your data grows. Because it runs efficiently on CPUs, Elasticsearch's full-text search requires minimal computational resources compared to GPU-intensive vector operations.
You can combine full-text search with [semantic search using vectors](https://www.elastic.co/docs/solutions/search/semantic-search) to build modern hybrid search applications. While vector search may require additional GPU resources, the full-text component remains cost-effective by leveraging existing CPU infrastructure.

## Getting started

For a high-level overview of how full-text search works, refer to [How full-text search works](https://www.elastic.co/docs/solutions/search/full-text/how-full-text-works).
For a hands-on introduction to full-text search, refer to the [full-text search tutorial](https://www.elastic.co/docs/reference/query-languages/query-dsl/full-text-filter-tutorial).

## Learn more

Here are some resources to help you learn more about full-text search with Elasticsearch.
**Core concepts**
Learn about the core components of full-text search:
- [Text fields](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/text)
- [Text analysis](https://www.elastic.co/docs/solutions/search/full-text/text-analysis-during-search)  
  - [Tokenizers](https://www.elastic.co/docs/reference/text-analysis/tokenizer-reference)
  - [Analyzers](https://www.elastic.co/docs/reference/text-analysis/analyzer-reference)

**Elasticsearch query languages**
Learn how to build full-text search queries using Elasticsearch's query languages:
- [Full-text queries using Query DSL](https://www.elastic.co/docs/reference/query-languages/query-dsl/full-text-queries)
- [Full-text search functions in ES|QL](https://www.elastic.co/docs/reference/query-languages/esql/functions-operators/search-functions)

**Advanced topics**
For a technical deep dive into Elasticsearch's BM25 implementation read this blog post: [The BM25 Algorithm and its Variables](https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables).
To learn how to optimize the relevance of your search results, refer to [Search relevance optimizations](https://www.elastic.co/docs/solutions/search/full-text/search-relevance).