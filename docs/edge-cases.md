# Edge Case Tests

This page has some test values.
It is also configured to not list backlinks.

## Invalid links

<a>link without target</a>

<a href="javascript:alert(1)">Link with JS target</a>

<a href="https://example.com">External link</a>

## Malformed links

<a href='/page-a.html">Mismatched quotes</a>

<a href="/page-a.html'>Mismatched quotes</a>


## Weird but OK links

<a href=/page-a/>No quotes</a>

<a href='/page-a/'>Single quotes</a>

<a href="/%70a%67e-%61/">URL encoding in target</a>

[URL encoding in Markdown](/%70a%67e-%61/)

[URL with spaces in it](https://example.com/Some File.txt)
