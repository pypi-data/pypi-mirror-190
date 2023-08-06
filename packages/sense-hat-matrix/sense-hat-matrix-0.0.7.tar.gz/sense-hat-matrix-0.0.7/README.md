# sense-hat-matrix
## Usage
```python
from sense_hat import SenseHat
from sense_hat_matrix.Graph import Graph
from sense_hat_matrix.GraphUtil import temp_colour
from sense_hat_matrix.GraphUtil import rescale

min_temp = 20
max_temp = 24
sense    = SenseHat()
temp     = sense.get_temperature()
g        = Graph(min_temp, max_temp)
pixels   = g.render(temp)
sense.set_pixels(pixels)
```

### Example project
   * [pi Weather Station](https://github.com/szigyi/pi-weather-station)

## Dev
### Install project
   * `pip3 install -e . `

### Release new version
[Create new release with new `tag` on `github`](https://github.com/szigyi/sense-hat-matrix/releases/new)

