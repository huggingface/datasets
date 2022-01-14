# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""RedCaps dataset."""


import collections
import json
import os
import re

import datasets


_CITATION = """\
@misc{desai2021redcaps,
      title={RedCaps: web-curated image-text data created by the people, for the people},
      author={Karan Desai and Gaurav Kaul and Zubin Aysola and Justin Johnson},
      year={2021},
      eprint={2111.11431},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
"""

_DESCRIPTION = """\
RedCaps is a large-scale dataset of 12M image-text pairs collected from Reddit.
Images and captions from Reddit depict and describe a wide variety of objects and scenes.
The data is collected from a manually curated set of subreddits (350 total),
which give coarse image labels and allow steering of the dataset composition
without labeling individual instances.
"""

_HOMEPAGE = "https://redcaps.xyz/"

_LICENSE = "CC BY 4.0"

_URL = "https://www.dropbox.com/s/cqtdpsl4hewlli1/redcaps_v1.0_annotations.zip?dl=1"

_SUBREDDITS_WITH_YEAR = """\
abandonedporn_2017 abandonedporn_2018 abandonedporn_2019 abandonedporn_2020 abandoned_2017 abandoned_2018
abandoned_2019 abandoned_2020 absoluteunits_2018 absoluteunits_2019 absoluteunits_2020 airplants_2017 airplants_2018
airplants_2019 airplants_2020 alltheanimals_2019 alltheanimals_2020 amateurphotography_2017 amateurphotography_2018
amateurphotography_2019 amateurphotography_2020 amateurroomporn_2017 amateurroomporn_2018 amateurroomporn_2019
amateurroomporn_2020 animalporn_2017 animalporn_2018 animalporn_2019 animalporn_2020 antiques_2017 antiques_2018
antiques_2019 antiques_2020 antkeeping_2017 antkeeping_2018 antkeeping_2019 antkeeping_2020 ants_2017 ants_2018
ants_2019 ants_2020 aquariums_2017 aquariums_2018 aquariums_2019 aquariums_2020 architectureporn_2017
architectureporn_2018 architectureporn_2019 architectureporn_2020 artefactporn_2017 artefactporn_2018 artefactporn_2019
artefactporn_2020 astronomy_2017 astronomy_2018 astronomy_2019 astronomy_2020 astrophotography_2017
astrophotography_2018 astrophotography_2019 astrophotography_2020 australiancattledog_2017 australiancattledog_2018
australiancattledog_2019 australiancattledog_2020 australianshepherd_2017 australianshepherd_2018
australianshepherd_2019 australianshepherd_2020 autumnporn_2017 autumnporn_2018 autumnporn_2019 autumnporn_2020
averagebattlestations_2017 averagebattlestations_2018 averagebattlestations_2019 averagebattlestations_2020
awwducational_2017 awwducational_2018 awwducational_2019 awwducational_2020 awwnverts_2017 awwnverts_2018
awwnverts_2019 awwnverts_2020 axolotls_2017 axolotls_2018 axolotls_2019 axolotls_2020 backpacking_2017 backpacking_2018
backpacking_2019 backpacking_2020 backyardchickens_2017 backyardchickens_2018 backyardchickens_2019
backyardchickens_2020 baking_2017 baking_2018 baking_2019 baking_2020 ballpython_2017 ballpython_2018 ballpython_2019
ballpython_2020 barista_2017 barista_2018 barista_2019 barista_2020 bassfishing_2017 bassfishing_2018 bassfishing_2019
bassfishing_2020 battlestations_2017 battlestations_2018 battlestations_2019 battlestations_2020 bbq_2017 bbq_2018
bbq_2019 bbq_2020 beagle_2017 beagle_2018 beagle_2019 beagle_2020 beardeddragons_2017 beardeddragons_2018
beardeddragons_2019 beardeddragons_2020 beekeeping_2017 beekeeping_2018 beekeeping_2019 beekeeping_2020
beerandpizza_2017 beerandpizza_2018 beerandpizza_2019 beerandpizza_2020 beerporn_2017 beerporn_2018 beerporn_2019
beerporn_2020 beerwithaview_2017 beerwithaview_2018 beerwithaview_2019 beerwithaview_2020 beginnerwoodworking_2017
beginnerwoodworking_2018 beginnerwoodworking_2019 beginnerwoodworking_2020 bengalcats_2017 bengalcats_2018
bengalcats_2019 bengalcats_2020 bento_2017 bento_2018 bento_2019 bento_2020 bernesemountaindogs_2017
bernesemountaindogs_2018 bernesemountaindogs_2019 bernesemountaindogs_2020 berries_2017 berries_2018 berries_2019
berries_2020 bettafish_2017 bettafish_2018 bettafish_2019 bettafish_2020 bicycling_2017 bicycling_2018 bicycling_2019
bicycling_2020 bikecommuting_2017 bikecommuting_2018 bikecommuting_2019 bikecommuting_2020 birding_2017 birding_2018
birding_2019 birding_2020 birdphotography_2017 birdphotography_2018 birdphotography_2019 birdphotography_2020
birdpics_2017 birdpics_2018 birdpics_2019 birdpics_2020 birdsofprey_2017 birdsofprey_2018 birdsofprey_2019
birdsofprey_2020 birds_2019 birds_2020 blackcats_2017 blackcats_2018 blackcats_2019 blackcats_2020 blacksmith_2017
blacksmith_2018 blacksmith_2019 blacksmith_2020 bladesmith_2017 bladesmith_2018 bladesmith_2019 bladesmith_2020
boatporn_2017 boatporn_2018 boatporn_2019 boatporn_2020 bonsai_2017 bonsai_2018 bonsai_2019 bonsai_2020 bookporn_2017
bookporn_2018 bookporn_2019 bookporn_2020 bookshelf_2017 bookshelf_2018 bookshelf_2019 bookshelf_2020 bordercollie_2017
bordercollie_2018 bordercollie_2019 bordercollie_2020 bostonterrier_2017 bostonterrier_2018 bostonterrier_2019
bostonterrier_2020 botanicalporn_2017 botanicalporn_2018 botanicalporn_2019 botanicalporn_2020 breadit_2017
breadit_2018 breadit_2019 breadit_2020 breakfastfood_2017 breakfastfood_2018 breakfastfood_2019 breakfastfood_2020
breakfast_2017 breakfast_2018 breakfast_2019 breakfast_2020 bridgeporn_2017 bridgeporn_2018 bridgeporn_2019
bridgeporn_2020 brochet_2017 brochet_2018 brochet_2019 brochet_2020 budgetfood_2017 budgetfood_2018 budgetfood_2019
budgetfood_2020 budgies_2017 budgies_2018 budgies_2019 budgies_2020 bulldogs_2017 bulldogs_2018 bulldogs_2019
bulldogs_2020 burgers_2017 burgers_2018 burgers_2019 burgers_2020 butterflies_2017 butterflies_2018 butterflies_2019
butterflies_2020 cabinporn_2017 cabinporn_2018 cabinporn_2019 cabinporn_2020 cactus_2017 cactus_2018 cactus_2019
cactus_2020 cakedecorating_2017 cakedecorating_2018 cakedecorating_2019 cakedecorating_2020 cakewin_2017 cakewin_2018
cakewin_2019 cakewin_2020 cameras_2017 cameras_2018 cameras_2019 cameras_2020 campingandhiking_2017
campingandhiking_2018 campingandhiking_2019 campingandhiking_2020 camping_2017 camping_2018 camping_2019 camping_2020
carnivorousplants_2017 carnivorousplants_2018 carnivorousplants_2019 carnivorousplants_2020 carpentry_2017
carpentry_2018 carpentry_2019 carpentry_2020 carporn_2017 carporn_2018 carporn_2019 carporn_2020 cassetteculture_2017
cassetteculture_2018 cassetteculture_2019 cassetteculture_2020 castiron_2017 castiron_2018 castiron_2019 castiron_2020
castles_2017 castles_2018 castles_2019 castles_2020 casualknitting_2017 casualknitting_2018 casualknitting_2019
casualknitting_2020 catpictures_2017 catpictures_2018 catpictures_2019 catpictures_2020 cats_2017 cats_2018 cats_2019
cats_2020 ceramics_2017 ceramics_2018 ceramics_2019 ceramics_2020 chameleons_2017 chameleons_2018 chameleons_2019
chameleons_2020 charcuterie_2017 charcuterie_2018 charcuterie_2019 charcuterie_2020 cheesemaking_2017 cheesemaking_2018
cheesemaking_2019 cheesemaking_2020 cheese_2017 cheese_2018 cheese_2019 cheese_2020 chefit_2017 chefit_2018 chefit_2019
chefit_2020 chefknives_2017 chefknives_2018 chefknives_2019 chefknives_2020 chickens_2017 chickens_2018 chickens_2019
chickens_2020 chihuahua_2017 chihuahua_2018 chihuahua_2019 chihuahua_2020 chinchilla_2017 chinchilla_2018
chinchilla_2019 chinchilla_2020 chinesefood_2017 chinesefood_2018 chinesefood_2019 chinesefood_2020 churchporn_2017
churchporn_2018 churchporn_2019 churchporn_2020 cider_2017 cider_2018 cider_2019 cider_2020 cityporn_2017 cityporn_2018
cityporn_2019 cityporn_2020 classiccars_2017 classiccars_2018 classiccars_2019 classiccars_2020 cockatiel_2017
cockatiel_2018 cockatiel_2019 cockatiel_2020 cocktails_2017 cocktails_2018 cocktails_2019 cocktails_2020
coffeestations_2017 coffeestations_2018 coffeestations_2019 coffeestations_2020 coins_2017 coins_2018 coins_2019
coins_2020 cookiedecorating_2017 cookiedecorating_2018 cookiedecorating_2019 cookiedecorating_2020 corgi_2017
corgi_2018 corgi_2019 corgi_2020 cornsnakes_2017 cornsnakes_2018 cornsnakes_2019 cornsnakes_2020 cozyplaces_2017
cozyplaces_2018 cozyplaces_2019 cozyplaces_2020 crafts_2017 crafts_2018 crafts_2019 crafts_2020 crestedgecko_2017
crestedgecko_2018 crestedgecko_2019 crestedgecko_2020 crochet_2017 crochet_2018 crochet_2019 crochet_2020
crossstitch_2017 crossstitch_2018 crossstitch_2019 crossstitch_2020 crows_2017 crows_2018 crows_2019 crows_2020
crystals_2017 crystals_2018 crystals_2019 crystals_2020 cupcakes_2017 cupcakes_2018 cupcakes_2019 cupcakes_2020
dachshund_2017 dachshund_2018 dachshund_2019 dachshund_2020 damnthatsinteresting_2017 damnthatsinteresting_2018
damnthatsinteresting_2019 damnthatsinteresting_2020 desertporn_2017 desertporn_2018 desertporn_2019 desertporn_2020
designmyroom_2017 designmyroom_2018 designmyroom_2019 designmyroom_2020 desksetup_2017 desksetup_2018 desksetup_2019
desksetup_2020 dessertporn_2017 dessertporn_2018 dessertporn_2019 dessertporn_2020 dessert_2017 dessert_2018
dessert_2019 dessert_2020 diy_2017 diy_2018 diy_2019 diy_2020 dobermanpinscher_2017 dobermanpinscher_2018
dobermanpinscher_2019 dobermanpinscher_2020 doggos_2017 doggos_2018 doggos_2019 doggos_2020 dogpictures_2017
dogpictures_2018 dogpictures_2019 dogpictures_2020 drunkencookery_2017 drunkencookery_2018 drunkencookery_2019
drunkencookery_2020 duck_2017 duck_2018 duck_2019 duck_2020 dumpsterdiving_2017 dumpsterdiving_2018 dumpsterdiving_2019
dumpsterdiving_2020 earthporn_2017 earthporn_2018 earthporn_2019 earthporn_2020 eatsandwiches_2017 eatsandwiches_2018
eatsandwiches_2019 eatsandwiches_2020 embroidery_2017 embroidery_2018 embroidery_2019 embroidery_2020 entomology_2017
entomology_2018 entomology_2019 entomology_2020 equestrian_2017 equestrian_2018 equestrian_2019 equestrian_2020
espresso_2017 espresso_2018 espresso_2019 espresso_2020 exposureporn_2017 exposureporn_2018 exposureporn_2019
exposureporn_2020 eyebleach_2017 eyebleach_2018 eyebleach_2019 eyebleach_2020 f1porn_2017 f1porn_2018 f1porn_2019
f1porn_2020 farming_2017 farming_2018 farming_2019 farming_2020 femalelivingspace_2017 femalelivingspace_2018
femalelivingspace_2019 femalelivingspace_2020 fermentation_2017 fermentation_2018 fermentation_2019 fermentation_2020
ferrets_2017 ferrets_2018 ferrets_2019 ferrets_2020 fireporn_2017 fireporn_2018 fireporn_2019 fireporn_2020
fishing_2017 fishing_2018 fishing_2019 fishing_2020 fish_2017 fish_2018 fish_2019 fish_2020 flowers_2017 flowers_2018
flowers_2019 flowers_2020 flyfishing_2017 flyfishing_2018 flyfishing_2019 flyfishing_2020 foodporn_2017 foodporn_2018
foodporn_2019 foodporn_2020 food_2017 food_2018 food_2019 food_2020 foraging_2017 foraging_2018 foraging_2019
foraging_2020 fossilporn_2017 fossilporn_2018 fossilporn_2019 fossilporn_2020 fountainpens_2017 fountainpens_2018
fountainpens_2019 fountainpens_2020 foxes_2017 foxes_2018 foxes_2019 foxes_2020 frenchbulldogs_2017 frenchbulldogs_2018
frenchbulldogs_2019 frenchbulldogs_2020 frogs_2017 frogs_2018 frogs_2019 frogs_2020 gardening_2017 gardening_2018
gardening_2019 gardening_2020 gardenwild_2017 gardenwild_2018 gardenwild_2019 gardenwild_2020 geckos_2017 geckos_2018
geckos_2019 geckos_2020 gemstones_2017 gemstones_2018 gemstones_2019 gemstones_2020 geologyporn_2017 geologyporn_2018
geologyporn_2019 geologyporn_2020 germanshepherds_2017 germanshepherds_2018 germanshepherds_2019 germanshepherds_2020
glutenfree_2017 glutenfree_2018 glutenfree_2019 glutenfree_2020 goldenretrievers_2017 goldenretrievers_2018
goldenretrievers_2019 goldenretrievers_2020 goldfish_2017 goldfish_2018 goldfish_2019 goldfish_2020 gold_2017 gold_2018
gold_2019 gold_2020 greatpyrenees_2017 greatpyrenees_2018 greatpyrenees_2019 greatpyrenees_2020 grilledcheese_2017
grilledcheese_2018 grilledcheese_2019 grilledcheese_2020 grilling_2017 grilling_2018 grilling_2019 grilling_2020
guineapigs_2017 guineapigs_2018 guineapigs_2019 guineapigs_2020 gunporn_2017 gunporn_2018 gunporn_2019 gunporn_2020
guns_2017 guns_2018 guns_2019 guns_2020 hamsters_2017 hamsters_2018 hamsters_2019 hamsters_2020 handtools_2017
handtools_2018 handtools_2019 handtools_2020 healthyfood_2017 healthyfood_2018 healthyfood_2019 healthyfood_2020
hedgehog_2017 hedgehog_2018 hedgehog_2019 hedgehog_2020 helicopters_2017 helicopters_2018 helicopters_2019
helicopters_2020 herpetology_2017 herpetology_2018 herpetology_2019 herpetology_2020 hiking_2017 hiking_2018
hiking_2019 hiking_2020 homestead_2017 homestead_2018 homestead_2019 homestead_2020 horses_2017 horses_2018 horses_2019
horses_2020 hotpeppers_2017 hotpeppers_2018 hotpeppers_2019 hotpeppers_2020 houseplants_2017 houseplants_2018
houseplants_2019 houseplants_2020 houseporn_2017 houseporn_2018 houseporn_2019 houseporn_2020 husky_2017 husky_2018
husky_2019 husky_2020 icecreamery_2017 icecreamery_2018 icecreamery_2019 icecreamery_2020 indoorgarden_2017
indoorgarden_2018 indoorgarden_2019 indoorgarden_2020 infrastructureporn_2017 infrastructureporn_2018
infrastructureporn_2019 infrastructureporn_2020 insects_2017 insects_2018 insects_2019 insects_2020 instantpot_2017
instantpot_2018 instantpot_2019 instantpot_2020 interestingasfuck_2017 interestingasfuck_2018 interestingasfuck_2019
interestingasfuck_2020 interiordesign_2017 interiordesign_2018 interiordesign_2019 interiordesign_2020
itookapicture_2017 itookapicture_2018 itookapicture_2019 itookapicture_2020 jellyfish_2017 jellyfish_2018
jellyfish_2019 jellyfish_2020 jewelry_2017 jewelry_2018 jewelry_2019 jewelry_2020 kayakfishing_2017 kayakfishing_2018
kayakfishing_2019 kayakfishing_2020 kayaking_2017 kayaking_2018 kayaking_2019 kayaking_2020 ketorecipes_2017
ketorecipes_2018 ketorecipes_2019 ketorecipes_2020 knifeporn_2017 knifeporn_2018 knifeporn_2019 knifeporn_2020
knives_2017 knives_2018 knives_2019 knives_2020 labrador_2017 labrador_2018 labrador_2019 labrador_2020
leathercraft_2017 leathercraft_2018 leathercraft_2019 leathercraft_2020 leopardgeckos_2017 leopardgeckos_2018
leopardgeckos_2019 leopardgeckos_2020 lizards_2017 lizards_2018 lizards_2019 lizards_2020 lookatmydog_2017
lookatmydog_2018 lookatmydog_2019 lookatmydog_2020 macarons_2017 macarons_2018 macarons_2019 macarons_2020
machineporn_2017 machineporn_2018 machineporn_2019 machineporn_2020 macroporn_2017 macroporn_2018 macroporn_2019
macroporn_2020 malelivingspace_2017 malelivingspace_2018 malelivingspace_2019 malelivingspace_2020 mead_2017 mead_2018
mead_2019 mead_2020 mealprepsunday_2017 mealprepsunday_2018 mealprepsunday_2019 mealprepsunday_2020
mechanicalkeyboards_2017 mechanicalkeyboards_2018 mechanicalkeyboards_2019 mechanicalkeyboards_2020
mechanicalpencils_2017 mechanicalpencils_2018 mechanicalpencils_2019 mechanicalpencils_2020 melts_2017 melts_2018
melts_2019 melts_2020 metalworking_2017 metalworking_2018 metalworking_2019 metalworking_2020 microgreens_2017
microgreens_2018 microgreens_2019 microgreens_2020 microporn_2017 microporn_2018 microporn_2019 microporn_2020
mildlyinteresting_2017 mildlyinteresting_2018 mildlyinteresting_2019 mildlyinteresting_2020 mineralporn_2017
mineralporn_2018 mineralporn_2019 mineralporn_2020 monitors_2017 monitors_2018 monitors_2019 monitors_2020
monstera_2018 monstera_2019 monstera_2020 mostbeautiful_2017 mostbeautiful_2018 mostbeautiful_2019 mostbeautiful_2020
motorcycleporn_2017 motorcycleporn_2018 motorcycleporn_2019 motorcycleporn_2020 muglife_2017 muglife_2018 muglife_2019
muglife_2020 mushroomgrowers_2017 mushroomgrowers_2018 mushroomgrowers_2019 mushroomgrowers_2020 mushroomporn_2017
mushroomporn_2018 mushroomporn_2019 mushroomporn_2020 mushrooms_2017 mushrooms_2018 mushrooms_2019 mushrooms_2020
mycology_2017 mycology_2018 mycology_2019 mycology_2020 natureisfuckinglit_2017 natureisfuckinglit_2018
natureisfuckinglit_2019 natureisfuckinglit_2020 natureporn_2017 natureporn_2018 natureporn_2019 natureporn_2020
nebelung_2017 nebelung_2018 nebelung_2019 nebelung_2020 orchids_2017 orchids_2018 orchids_2019 orchids_2020 otters_2017
otters_2018 otters_2019 otters_2020 outdoors_2017 outdoors_2018 outdoors_2019 outdoors_2020 owls_2017 owls_2018
owls_2019 owls_2020 parrots_2017 parrots_2018 parrots_2019 parrots_2020 pelletgrills_2017 pelletgrills_2018
pelletgrills_2019 pelletgrills_2020 pens_2017 pens_2018 pens_2019 pens_2020 perfectfit_2017 perfectfit_2018
perfectfit_2019 perfectfit_2020 permaculture_2017 permaculture_2018 permaculture_2019 permaculture_2020
photocritique_2017 photocritique_2018 photocritique_2019 photocritique_2020 photographs_2017 photographs_2018
photographs_2019 photographs_2020 pics_2017 pics_2018 pics_2019 pics_2020 pitbulls_2017 pitbulls_2018 pitbulls_2019
pitbulls_2020 pizza_2017 pizza_2018 pizza_2019 pizza_2020 plantbaseddiet_2017 plantbaseddiet_2018 plantbaseddiet_2019
plantbaseddiet_2020 plantedtank_2017 plantedtank_2018 plantedtank_2019 plantedtank_2020 plantsandpots_2019
plantsandpots_2020 plants_2017 plants_2018 plants_2019 plants_2020 pomeranians_2017 pomeranians_2018 pomeranians_2019
pomeranians_2020 pottery_2017 pottery_2018 pottery_2019 pottery_2020 pourpainting_2017 pourpainting_2018
pourpainting_2019 pourpainting_2020 proplifting_2017 proplifting_2018 proplifting_2019 proplifting_2020 pugs_2017
pugs_2018 pugs_2019 pugs_2020 pug_2017 pug_2018 pug_2019 pug_2020 quilting_2017 quilting_2018 quilting_2019
quilting_2020 rabbits_2017 rabbits_2018 rabbits_2019 rabbits_2020 ramen_2017 ramen_2018 ramen_2019 ramen_2020
rarepuppers_2017 rarepuppers_2018 rarepuppers_2019 rarepuppers_2020 reeftank_2017 reeftank_2018 reeftank_2019
reeftank_2020 reptiles_2017 reptiles_2018 reptiles_2019 reptiles_2020 resincasting_2017 resincasting_2018
resincasting_2019 resincasting_2020 roomporn_2017 roomporn_2018 roomporn_2019 roomporn_2020 roses_2017 roses_2018
roses_2019 roses_2020 rottweiler_2017 rottweiler_2018 rottweiler_2019 rottweiler_2020 ruralporn_2017 ruralporn_2018
ruralporn_2019 ruralporn_2020 sailing_2017 sailing_2018 sailing_2019 sailing_2020 salsasnobs_2018 salsasnobs_2019
salsasnobs_2020 samoyeds_2017 samoyeds_2018 samoyeds_2019 samoyeds_2020 savagegarden_2017 savagegarden_2018
savagegarden_2019 savagegarden_2020 scotch_2017 scotch_2018 scotch_2019 scotch_2020 seaporn_2017 seaporn_2018
seaporn_2019 seaporn_2020 seriouseats_2017 seriouseats_2018 seriouseats_2019 seriouseats_2020 sewing_2017 sewing_2018
sewing_2019 sewing_2020 sharks_2017 sharks_2018 sharks_2019 sharks_2020 shiba_2017 shiba_2018 shiba_2019 shiba_2020
shihtzu_2017 shihtzu_2018 shihtzu_2019 shihtzu_2020 shrimptank_2017 shrimptank_2018 shrimptank_2019 shrimptank_2020
siamesecats_2017 siamesecats_2018 siamesecats_2019 siamesecats_2020 siberiancats_2017 siberiancats_2018
siberiancats_2019 siberiancats_2020 silverbugs_2017 silverbugs_2018 silverbugs_2019 silverbugs_2020 skyporn_2017
skyporn_2018 skyporn_2019 skyporn_2020 sloths_2017 sloths_2018 sloths_2019 sloths_2020 smoking_2017 smoking_2018
smoking_2019 smoking_2020 snails_2017 snails_2018 snails_2019 snails_2020 snakes_2017 snakes_2018 snakes_2019
snakes_2020 sneakers_2017 sneakers_2018 sneakers_2019 sneakers_2020 sneks_2017 sneks_2018 sneks_2019 sneks_2020
somethingimade_2017 somethingimade_2018 somethingimade_2019 somethingimade_2020 soup_2017 soup_2018 soup_2019 soup_2020
sourdough_2017 sourdough_2018 sourdough_2019 sourdough_2020 sousvide_2017 sousvide_2018 sousvide_2019 sousvide_2020
spaceporn_2017 spaceporn_2018 spaceporn_2019 spaceporn_2020 spicy_2017 spicy_2018 spicy_2019 spicy_2020 spiderbro_2017
spiderbro_2018 spiderbro_2019 spiderbro_2020 spiders_2017 spiders_2018 spiders_2019 spiders_2020 squirrels_2017
squirrels_2018 squirrels_2019 squirrels_2020 steak_2017 steak_2018 steak_2019 steak_2020 streetphotography_2017
streetphotography_2018 streetphotography_2019 streetphotography_2020 succulents_2017 succulents_2018 succulents_2019
succulents_2020 superbowl_2017 superbowl_2018 superbowl_2019 superbowl_2020 supermodelcats_2017 supermodelcats_2018
supermodelcats_2019 supermodelcats_2020 sushi_2017 sushi_2018 sushi_2019 sushi_2020 tacos_2017 tacos_2018 tacos_2019
tacos_2020 tarantulas_2017 tarantulas_2018 tarantulas_2019 tarantulas_2020 tastyfood_2017 tastyfood_2018 tastyfood_2019
tastyfood_2020 teaporn_2017 teaporn_2018 teaporn_2019 teaporn_2020 tea_2017 tea_2018 tea_2019 tea_2020 tequila_2017
tequila_2018 tequila_2019 tequila_2020 terrariums_2017 terrariums_2018 terrariums_2019 terrariums_2020
thedepthsbelow_2017 thedepthsbelow_2018 thedepthsbelow_2019 thedepthsbelow_2020 thriftstorehauls_2017
thriftstorehauls_2018 thriftstorehauls_2019 thriftstorehauls_2020 tinyanimalsonfingers_2017 tinyanimalsonfingers_2018
tinyanimalsonfingers_2019 tinyanimalsonfingers_2020 tonightsdinner_2017 tonightsdinner_2018 tonightsdinner_2019
tonightsdinner_2020 toolporn_2017 toolporn_2018 toolporn_2019 toolporn_2020 tools_2017 tools_2018 tools_2019 tools_2020
torties_2017 torties_2018 torties_2019 torties_2020 tortoise_2017 tortoise_2018 tortoise_2019 tortoise_2020
tractors_2017 tractors_2018 tractors_2019 tractors_2020 trailrunning_2017 trailrunning_2018 trailrunning_2019
trailrunning_2020 trains_2017 trains_2018 trains_2019 trains_2020 trucks_2017 trucks_2018 trucks_2019 trucks_2020
turtle_2017 turtle_2018 turtle_2019 turtle_2020 underwaterphotography_2017 underwaterphotography_2018
underwaterphotography_2019 underwaterphotography_2020 upcycling_2017 upcycling_2018 upcycling_2019 upcycling_2020
urbanexploration_2017 urbanexploration_2018 urbanexploration_2019 urbanexploration_2020 urbanhell_2017 urbanhell_2018
urbanhell_2019 urbanhell_2020 veganfoodporn_2017 veganfoodporn_2018 veganfoodporn_2019 veganfoodporn_2020
veganrecipes_2017 veganrecipes_2018 veganrecipes_2019 veganrecipes_2020 vegetablegardening_2017 vegetablegardening_2018
vegetablegardening_2019 vegetablegardening_2020 vegetarian_2017 vegetarian_2018 vegetarian_2019 vegetarian_2020
villageporn_2017 villageporn_2018 villageporn_2019 villageporn_2020 vintageaudio_2017 vintageaudio_2018
vintageaudio_2019 vintageaudio_2020 vintage_2017 vintage_2018 vintage_2019 vintage_2020 vinyl_2017 vinyl_2018
vinyl_2019 vinyl_2020 volumeeating_2017 volumeeating_2018 volumeeating_2019 volumeeating_2020 watches_2017 watches_2018
watches_2019 watches_2020 waterporn_2017 waterporn_2018 waterporn_2019 waterporn_2020 weatherporn_2017 weatherporn_2018
weatherporn_2019 weatherporn_2020 wewantplates_2017 wewantplates_2018 wewantplates_2019 wewantplates_2020
wildernessbackpacking_2017 wildernessbackpacking_2018 wildernessbackpacking_2019 wildernessbackpacking_2020
wildlifephotography_2017 wildlifephotography_2018 wildlifephotography_2019 wildlifephotography_2020 wine_2017 wine_2018
wine_2019 wine_2020 winterporn_2017 winterporn_2018 winterporn_2019 winterporn_2020 woodcarving_2017 woodcarving_2018
woodcarving_2019 woodcarving_2020 woodworking_2017 woodworking_2018 woodworking_2019 woodworking_2020 workbenches_2017
workbenches_2018 workbenches_2019 workbenches_2020 workspaces_2017 workspaces_2018 workspaces_2019 workspaces_2020
yarnaddicts_2017 yarnaddicts_2018 yarnaddicts_2019 yarnaddicts_2020 zerowaste_2017 zerowaste_2018 zerowaste_2019
zerowaste_2020
"""
_SUBREDDITS_WITH_YEAR = _SUBREDDITS_WITH_YEAR.strip().split()

_SUBREDDIT_TO_YEAR = collections.defaultdict(list)
for subreddit_with_year in _SUBREDDITS_WITH_YEAR:
    subreddit, year = subreddit_with_year.split("_")
    _SUBREDDIT_TO_YEAR[subreddit].append(year)

_SUBREDDITS = list(_SUBREDDIT_TO_YEAR.keys())


def _config_name_to_subreddits_with_year(config_name):
    if config_name == "all":
        return _SUBREDDITS_WITH_YEAR
    elif re.match(r".*_\d{4}$", config_name):
        return [config_name]
    else:
        return [f"{config_name}_{year}" for year in _SUBREDDIT_TO_YEAR[config_name]]


def _config_name_to_description(config_name):
    if config_name == "all":
        return "Contains data from all the subreddits"
    else:
        if re.match(r".*_\d{4}$", config_name):
            subreddit, year = config_name.split("_")
            year_str = "2008 - 2017" if year == "2017" else year
        else:
            subreddit = config_name
            year_str = ", ".join(
                ["2008 - 2017" if year == "2017" else year for year in _SUBREDDIT_TO_YEAR[config_name]]
            )
        return f"Contains data from the {subreddit} subreddit posted in {year_str}"


class RedCapsConfig(datasets.BuilderConfig):
    """BuilderConfig for RedCaps."""

    def __init__(self, name, **kwargs):
        """BuilderConfig for RedCaps.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        assert "description" not in kwargs
        kwargs["description"] = _config_name_to_description(name)
        super(RedCapsConfig, self).__init__(version=datasets.Version("1.0.0", ""), name=name, **kwargs)


class RedCaps(datasets.GeneratorBasedBuilder):
    """RedCaps dataset."""

    BUILDER_CONFIGS = [
        RedCapsConfig("all"),
    ]
    BUILDER_CONFIGS += [RedCapsConfig(subreddit) for subreddit in _SUBREDDITS]
    BUILDER_CONFIGS += [RedCapsConfig(subreddit_with_year) for subreddit_with_year in _SUBREDDITS_WITH_YEAR]

    DEFAULT_CONFIG_NAME = "all"

    def _info(self):
        features = datasets.Features(
            {
                "image_id": datasets.Value("string"),
                "author": datasets.Value("string"),
                "image_url": datasets.Value("string"),
                "raw_caption": datasets.Value("string"),
                "caption": datasets.Value("string"),
                "subreddit": datasets.ClassLabel(names=_SUBREDDITS),
                "score": datasets.Value("int32"),
                "created_utc": datasets.Value("timestamp[s, tz=UTC]"),
                "permalink": datasets.Value("string"),
                "crosspost_parents": datasets.Sequence(datasets.Value("string")),
            }
        )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        annotations_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "annotations_dir": annotations_dir,
                    "subreddits": _config_name_to_subreddits_with_year(self.config.name),
                },
            ),
        ]

    def _generate_examples(self, annotations_dir, subreddits):
        annotations_dir = os.path.join(annotations_dir, "annotations")
        idx = 0
        for subreddit in subreddits:
            subreddit_file = os.path.join(annotations_dir, subreddit + ".json")
            with open(subreddit_file, encoding="utf-8") as f:
                data = json.load(f)
                for annot in data["annotations"]:
                    yield idx, {
                        "image_id": annot["image_id"],
                        "author": annot["author"],
                        "image_url": annot["url"],
                        "raw_caption": annot["raw_caption"],
                        "caption": annot["caption"],
                        "subreddit": annot["subreddit"],
                        "score": annot["score"] if "score" in annot else None,
                        "created_utc": annot["created_utc"],
                        "permalink": annot["permalink"],
                        "crosspost_parents": annot["crosspost_parents"]
                        if "crosspost_parents" in annot and annot["crosspost_parents"]
                        else None,
                    }
                    idx += 1
