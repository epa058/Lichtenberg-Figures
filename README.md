
# Lichtenberg Figures

*Currently working on a dielectric breakdown model algorithm. I GOT IT!*

This algorithm was developed in an attempt to best simulate the behaviour of an electric current travelling through an inhomogeneous, insulating material following dielectric breakdown.

The folder **Source Codes (Attempt 1)** contains Python scripts of my first attempt. After working on the single-branch algorithm, I mistakenly implemented depth-first search (DFS) rather than breadth-first search (BFS) for my multi-branch algorithm (I'm no CS major). In the end, my friend Shan Gao helped me develop the final, multi-branch BFS version of this algorithm.

The folder **Animations (Attempt 1)** contains a few animations from certain versions of this first attempt. Unfortunately, the patterns generated in this attempt appear unphysical and do not at all resemble Lichtenberg figures.

The folder **Source Codes (Attempt 2)** contains Python scripts of my latest attempt. For this attempt, I decided to actually read some papers about diffusion-limited aggregation (DLA) and the dielectric breakdown model (DBM). The papers I used as references are mentioned below. I then wrote two different algorithms: the single-tree algorithm and the double-tree algorithm. 

The folder **Animations (Attempt 2)** contains a few selected animations from certain versions of this second attempt. The patterns generated in this attempt are much more realistic and finally resemble Lichtenberg figures.

## Authors

- [@epa058](https://github.com/epa058)
- [@kosan](https://github.com/shan-gao5)


## Acknowledgements

 Thanks Andrew! Thanks Oscar! Thanks Sebastian! Thanks Fernando! Thanks Shan! \**applause\**


## Documentation

Hold on, I'm about to get on arXiv!! Nevermind, got rejected :( 

Here: [Discount Documentation](https://github.com/epa058/Lichtenberg-Figures/blob/main/Paper.pdf)


## Real References
- L. Niemeyer, L. Pietronero, and H. J. Wiesmann, "Fractal Dimensions of Dielectric Breakdown," *Physical Review Letters*, vol. 52, no. 12, pp. 1033-1036, 1984.
- L. Pietronero and H. J. Wiesmann, "Stochastic Model for Dielectric Breakdown," *Journal of Statistical Physics*, vol. 36, pp. 909-916, 1984.
- A. A. Tsonis and J. B. Elsner, "Fractal Characterization and Simulation of Lightning," *Beiträge zur Physik der Atmosphäre*, vol. 60, no. 2, pp. 187-192, 1987.


## Related

- [Yale: Diffusion-Limited Aggregation](https://web.archive.org/web/20030805085849/http://classes.yale.edu/fractals/Panorama/Physics/DLA/DLA.html)
- [chromia: lichtenberg](https://github.com/chromia/lichtenberg)
- [goedel-gang: lightning](https://github.com/goedel-gang/lightning)
- [neut: neutenpoel](https://github.com/neut/neutenpoel)
- [stompchicken: lichtenberg](https://github.com/stompchicken/lichtenberg)


## License

GNU General Public License v3.0


## Features

- Create your own custom grids!
- Choose your own starting positions! (you no longer get to do this with the new algorithms because I said so)
- Live animations!

That's about it :/


## FAQ

#### Q: Why did you start this project?

A: A while back, I saw a few people on YouTube [making Lichtenberg figures on wood](https://www.youtube.com/watch?v=BxjtCAp9JWo) and thought that it looked cool. Since I didn't [lack a sufficient amount of self-preservation](https://www.woodturner.org/Woodturner/Woodturner/Resources/Safety-Materials/Safety-Fractal-Burning-Lichtenburg-Burning.aspx), I thought it'd be a better idea to simulate it on the computer instead.

#### Q: Your figures don't really look like Lichtenberg figures...

A: That was a valid criticism back in 2022. Now you're just being picky.

#### Q: Why can we no longer set our own starting positions for algorithms 3 and 4?

A: Because I said so.


## Feedback

If you have any feedback, I'd like to hear it! Here's my email: epa058@gmail.com
