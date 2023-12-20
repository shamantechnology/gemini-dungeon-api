# Gemini Dungeon API

## Setup
### Environment

You should create a virtualenv with the required dependencies by running
```
make virtualenv
```

When a new requirement is needed you should add it to `unpinned_requirements.txt` and run
```
make update-requirements-txt
make virtualenv
```
this ensures that all requirements are pinned and work together for ensuring reproducibility

### Story

To setup the story of your adventure, create a .txt file with the story in a folder called "data" in the "src" folder. 

Story example of gemini's maze

```
In the heart of a dense and mysterious jungle lies the fabled lost treasure of Mu, whispered to hold unimaginable riches and ancient artifacts. Rumors spread among adventurers, enticing them to brave the perilous journey in search of this elusive bounty. As fate would have it, our valiant heroes stumble upon an enigmatic maze, shrouded in arcane magic and guarded by the formidable Wizard Gemini.

Unbeknownst to the intrepid explorers, this labyrinthine puzzle is a manifestation of Gemini's cunning intellect and magical prowess. Each twisting corridor and perplexing intersection within the maze poses deadly challenges—traps triggered by misplaced steps, illusions designed to deceive, and guardians that test the mettle of any who dare to seek the treasure.

Survival demands more than just physical prowess; it requires wit, teamwork, and clever problem-solving. The adventurers find themselves pitted against not only the maze's treacherous obstacles but also the calculated machinations of Gemini, who watches their progress with keen interest. The Wizard's intentions remain veiled, his motives elusive, as if the maze itself is an elaborate game for Gemini's amusement.

Amidst the harrowing trials and ever-shifting pathways, the adventurers must rely on their skills and instincts, forging alliances and unraveling the maze's secrets to reach the heart of this twisted labyrinth. Only there, at the maze's center, will they confront Gemini—a masterful wizard whose powers seem boundless and whose control over the maze is absolute.

As clashes between magic and might ensue, the fate of the treasure and the adventurers hangs in the balance. Will they outsmart the cunning Wizard Gemini, or will they become yet another footnote in the maze's history, forever entwined in its mystifying depths?
```