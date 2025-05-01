# JSON vs. IJSON

The current implementation of the demo data server uses a library called Iterative JSON Parser (ijson), which is a highly memory-efficient way of parsing large JSON files. Ijson parses files incrementally, line by line, without loading the entire file into memory first. As a result, it maintains a small memory footprint (~10-20 MB). However, the downside of this approach is that ijson cannot randomly access a specific position within the file, which, in our project, could be a particular tick or a specific point in time.

Python's built-in json library loads the entire JSON file into main memory and then parses it. Typically, an 800-900 MB JSON file consumes about 1500-2000 MB of memory when loaded. Consequently, this method is unsuitable for example container environments with limited memory resources (i.e. TiKe's OpenShift). However, if memory consumption is less of a concern, this approach has the advantage of quickly locating specific ticks or points in time. This capability would allow features like timeline control from the client side.

Switching from the ijson implementation to Python's built-in json library would be relatively straightforward. However, it would require adjustments in related components, especially the single client tick burst streaming.

### IJSON

- https://pypi.org/project/ijson/
- https://github.com/ICRAR/ijson