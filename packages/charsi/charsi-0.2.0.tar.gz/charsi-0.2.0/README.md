# Charsi

![Charis](./docs/images/charsi-x16.png) **Charsi** is a command-line tool to
help game modders build string resources for [Diablo II: Resurrected][1].

## Quickstart

1. Extract `item-names.json` file at `/data/local/lng/strings` from game data
   storage by [CascView](http://www.zezula.net/en/casc/main.html).

2. Write a recipe file `example.recipe` with following:

```
Text[qf1]: Example
```

3. Run the following command to build a new string table:

```
charsi build --recipe-file=example.recipe item-names.json > new-item-names.json
```

4. Replace file `/data/local/lng/strings/item-names.json`
   with `new-item-names.json` in your mods.

5. Check in game, item name `Khalim's Flail` has been replaced with `Example`.

## License

Copyright (C) 2022 HE Yaowen <he.yaowen@hotmail.com>

The GNU General Public License (GPL) version 3, see [LICENSE](./LICENSE).

[1]: https://diablo2.blizzard.com
