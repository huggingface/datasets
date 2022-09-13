# Copyright 2022 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""MIT Scene Parsing Benchmark."""


import os

import pandas as pd

import datasets


_CITATION = """\
@inproceedings{zhou2017scene,
    title={Scene Parsing through ADE20K Dataset},
    author={Zhou, Bolei and Zhao, Hang and Puig, Xavier and Fidler, Sanja and Barriuso, Adela and Torralba, Antonio},
    booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition},
    year={2017}
}

@article{zhou2016semantic,
  title={Semantic understanding of scenes through the ade20k dataset},
  author={Zhou, Bolei and Zhao, Hang and Puig, Xavier and Fidler, Sanja and Barriuso, Adela and Torralba, Antonio},
  journal={arXiv preprint arXiv:1608.05442},
  year={2016}
}
"""

_DESCRIPTION = """\
Scene parsing is to segment and parse an image into different image regions associated with semantic categories, such as sky, road, person, and bed.
MIT Scene Parsing Benchmark (SceneParse150) provides a standard training and evaluation platform for the algorithms of scene parsing.
The data for this benchmark comes from ADE20K Dataset which contains more than 20K scene-centric images exhaustively annotated with objects and object parts.
Specifically, the benchmark is divided into 20K images for training, 2K images for validation, and another batch of held-out images for testing.
There are totally 150 semantic categories included for evaluation, which include stuffs like sky, road, grass, and discrete objects like person, car, bed.
Note that there are non-uniform distribution of objects occuring in the images, mimicking a more natural object occurrence in daily scene.
"""

_HOMEPAGE = "http://sceneparsing.csail.mit.edu/"

_LICENSE = "BSD 3-Clause License"

_URLS = {
    "scene_parsing": {
        "train/val": "http://data.csail.mit.edu/places/ADEchallenge/ADEChallengeData2016.zip",
        "test": "http://data.csail.mit.edu/places/ADEchallenge/release_test.zip",
    },
    "instance_segmentation": {
        "images": "http://sceneparsing.csail.mit.edu/data/ChallengeData2017/images.tar",
        "annotations": "http://sceneparsing.csail.mit.edu/data/ChallengeData2017/annotations_instance.tar",
        "test": "http://sceneparsing.csail.mit.edu/data/ChallengeData2017/release_test.tar",
    },
}

_SCENE_CATEGORIES = """\
airport_terminal art_gallery badlands ball_pit bathroom beach bedroom booth_indoor botanical_garden bridge bullring
bus_interior butte canyon casino_outdoor castle church_outdoor closet coast conference_room construction_site corral
corridor crosswalk day_care_center sand elevator_interior escalator_indoor forest_road gangplank gas_station
golf_course gymnasium_indoor harbor hayfield heath hoodoo house hunting_lodge_outdoor ice_shelf joss_house kiosk_indoor
kitchen landfill library_indoor lido_deck_outdoor living_room locker_room market_outdoor mountain_snowy office orchard
arbor bookshelf mews nook preserve traffic_island palace palace_hall pantry patio phone_booth establishment
poolroom_home quonset_hut_outdoor rice_paddy sandbox shopfront skyscraper stone_circle subway_interior platform
supermarket swimming_pool_outdoor television_studio indoor_procenium train_railway coral_reef viaduct wave wind_farm
bottle_storage abbey access_road air_base airfield airlock airplane_cabin airport entrance airport_ticket_counter
alcove alley amphitheater amusement_arcade amusement_park anechoic_chamber apartment_building_outdoor apse_indoor
apse_outdoor aquarium aquatic_theater aqueduct arcade arch archaelogical_excavation archive basketball football hockey
performance rodeo soccer armory army_base arrival_gate_indoor arrival_gate_outdoor art_school art_studio artists_loft
assembly_line athletic_field_indoor athletic_field_outdoor atrium_home atrium_public attic auditorium auto_factory
auto_mechanics_indoor auto_mechanics_outdoor auto_racing_paddock auto_showroom backstage backstairs
badminton_court_indoor badminton_court_outdoor baggage_claim shop exterior balcony_interior ballroom bamboo_forest
bank_indoor bank_outdoor bank_vault banquet_hall baptistry_indoor baptistry_outdoor bar barbershop barn barndoor
barnyard barrack baseball_field basement basilica basketball_court_indoor basketball_court_outdoor bathhouse
batters_box batting_cage_indoor batting_cage_outdoor battlement bayou bazaar_indoor bazaar_outdoor beach_house
beauty_salon bedchamber beer_garden beer_hall belfry bell_foundry berth berth_deck betting_shop bicycle_racks bindery
biology_laboratory bistro_indoor bistro_outdoor bleachers_indoor bleachers_outdoor boardwalk boat_deck boathouse bog
bomb_shelter_indoor bookbindery bookstore bow_window_indoor bow_window_outdoor bowling_alley box_seat boxing_ring
breakroom brewery_indoor brewery_outdoor brickyard_indoor brickyard_outdoor building_complex building_facade bullpen
burial_chamber bus_depot_indoor bus_depot_outdoor bus_shelter bus_station_indoor bus_station_outdoor butchers_shop
cabana cabin_indoor cabin_outdoor cafeteria call_center campsite campus natural urban candy_store canteen
car_dealership backseat frontseat caravansary cardroom cargo_container_interior airplane boat freestanding
carport_indoor carport_outdoor carrousel casino_indoor catacomb cathedral_indoor cathedral_outdoor catwalk
cavern_indoor cavern_outdoor cemetery chalet chaparral chapel checkout_counter cheese_factory chemical_plant
chemistry_lab chicken_coop_indoor chicken_coop_outdoor chicken_farm_indoor chicken_farm_outdoor childs_room
choir_loft_interior church_indoor circus_tent_indoor circus_tent_outdoor city classroom clean_room cliff booth room
clock_tower_indoor cloister_indoor cloister_outdoor clothing_store coast_road cockpit coffee_shop computer_room
conference_center conference_hall confessional control_room control_tower_indoor control_tower_outdoor
convenience_store_indoor convenience_store_outdoor corn_field cottage cottage_garden courthouse courtroom courtyard
covered_bridge_interior crawl_space creek crevasse library cybercafe dacha dairy_indoor dairy_outdoor dam dance_school
darkroom delicatessen dentists_office department_store departure_lounge vegetation desert_road diner_indoor
diner_outdoor dinette_home vehicle dining_car dining_hall dining_room dirt_track discotheque distillery ditch dock
dolmen donjon doorway_indoor doorway_outdoor dorm_room downtown drainage_ditch dress_shop dressing_room drill_rig
driveway driving_range_indoor driving_range_outdoor drugstore dry_dock dugout earth_fissure editing_room
electrical_substation elevated_catwalk door freight_elevator elevator_lobby elevator_shaft embankment embassy
engine_room entrance_hall escalator_outdoor escarpment estuary excavation exhibition_hall fabric_store factory_indoor
factory_outdoor fairway farm fastfood_restaurant fence cargo_deck ferryboat_indoor passenger_deck cultivated wild
field_road fire_escape fire_station firing_range_indoor firing_range_outdoor fish_farm fishmarket fishpond
fitting_room_interior fjord flea_market_indoor flea_market_outdoor floating_dry_dock flood florist_shop_indoor
florist_shop_outdoor fly_bridge food_court football_field broadleaf needleleaf forest_fire forest_path formal_garden
fort fortress foundry_indoor foundry_outdoor fountain freeway funeral_chapel funeral_home furnace_room galley game_room
garage_indoor garage_outdoor garbage_dump gasworks gate gatehouse gazebo_interior general_store_indoor
general_store_outdoor geodesic_dome_indoor geodesic_dome_outdoor ghost_town gift_shop glacier glade gorge granary
great_hall greengrocery greenhouse_indoor greenhouse_outdoor grotto guardhouse gulch gun_deck_indoor gun_deck_outdoor
gun_store hacienda hallway handball_court hangar_indoor hangar_outdoor hardware_store hat_shop hatchery hayloft hearth
hedge_maze hedgerow heliport herb_garden highway hill home_office home_theater hospital hospital_room hot_spring
hot_tub_indoor hot_tub_outdoor hotel_outdoor hotel_breakfast_area hotel_room hunting_lodge_indoor hut ice_cream_parlor
ice_floe ice_skating_rink_indoor ice_skating_rink_outdoor iceberg igloo imaret incinerator_indoor incinerator_outdoor
industrial_area industrial_park inn_indoor inn_outdoor irrigation_ditch islet jacuzzi_indoor jacuzzi_outdoor
jail_indoor jail_outdoor jail_cell japanese_garden jetty jewelry_shop junk_pile junkyard jury_box kasbah kennel_indoor
kennel_outdoor kindergarden_classroom kiosk_outdoor kitchenette lab_classroom labyrinth_indoor labyrinth_outdoor lagoon
artificial landing landing_deck laundromat lava_flow lavatory lawn lean-to lecture_room legislative_chamber levee
library_outdoor lido_deck_indoor lift_bridge lighthouse limousine_interior liquor_store_indoor liquor_store_outdoor
loading_dock lobby lock_chamber loft lookout_station_indoor lookout_station_outdoor lumberyard_indoor
lumberyard_outdoor machine_shop manhole mansion manufactured_home market_indoor marsh martial_arts_gym mastaba
maternity_ward mausoleum medina menhir mesa mess_hall mezzanine military_hospital military_hut military_tent mine
mineshaft mini_golf_course_indoor mini_golf_course_outdoor mission dry water mobile_home monastery_indoor
monastery_outdoor moon_bounce moor morgue mosque_indoor mosque_outdoor motel mountain mountain_path mountain_road
movie_theater_indoor movie_theater_outdoor mudflat museum_indoor museum_outdoor music_store music_studio misc
natural_history_museum naval_base newsroom newsstand_indoor newsstand_outdoor nightclub nuclear_power_plant_indoor
nuclear_power_plant_outdoor nunnery nursery nursing_home oasis oast_house observatory_indoor observatory_outdoor
observatory_post ocean office_building office_cubicles oil_refinery_indoor oil_refinery_outdoor oilrig operating_room
optician organ_loft_interior orlop_deck ossuary outcropping outhouse_indoor outhouse_outdoor overpass oyster_bar
oyster_farm acropolis aircraft_carrier_object amphitheater_indoor archipelago questionable assembly_hall assembly_plant
awning_deck back_porch backdrop backroom backstage_outdoor backstairs_indoor backwoods ballet balustrade barbeque
basin_outdoor bath_indoor bath_outdoor bathhouse_outdoor battlefield bay booth_outdoor bottomland breakfast_table
bric-a-brac brooklet bubble_chamber buffet bulkhead bunk_bed bypass byroad cabin_cruiser cargo_helicopter cellar
chair_lift cocktail_lounge corner country_house country_road customhouse dance_floor deck-house_boat_deck_house
deck-house_deck_house dining_area diving_board embrasure entranceway_indoor entranceway_outdoor entryway_outdoor
estaminet farm_building farmhouse feed_bunk field_house field_tent_indoor field_tent_outdoor fire_trench fireplace
flashflood flatlet floating_dock flood_plain flowerbed flume_indoor flying_buttress foothill forecourt foreshore
front_porch garden gas_well glen grape_arbor grove guardroom guesthouse gymnasium_outdoor head_shop hen_yard hillock
housing_estate housing_project howdah inlet insane_asylum outside juke_joint jungle kraal laboratorywet landing_strip
layby lean-to_tent loge loggia_outdoor lower_deck luggage_van mansard meadow meat_house megalith mens_store_outdoor
mental_institution_indoor mental_institution_outdoor military_headquarters millpond millrace natural_spring
nursing_home_outdoor observation_station open-hearth_furnace operating_table outbuilding palestra parkway patio_indoor
pavement pawnshop_outdoor pinetum piste_road pizzeria_outdoor powder_room pumping_station reception_room rest_stop
retaining_wall rift_valley road rock_garden rotisserie safari_park salon saloon sanatorium science_laboratory scrubland
scullery seaside semidesert shelter shelter_deck shelter_tent shore shrubbery sidewalk snack_bar snowbank stage_set
stall stateroom store streetcar_track student_center study_hall sugar_refinery sunroom supply_chamber t-bar_lift
tannery teahouse threshing_floor ticket_window_indoor tidal_basin tidal_river tiltyard tollgate tomb tract_housing
trellis truck_stop upper_balcony vestibule vinery walkway war_room washroom water_fountain water_gate waterscape
waterway wetland widows_walk_indoor windstorm packaging_plant pagoda paper_mill park parking_garage_indoor
parking_garage_outdoor parking_lot parlor particle_accelerator party_tent_indoor party_tent_outdoor pasture pavilion
pawnshop pedestrian_overpass_indoor penalty_box pet_shop pharmacy physics_laboratory piano_store picnic_area pier
pig_farm pilothouse_indoor pilothouse_outdoor pitchers_mound pizzeria planetarium_indoor planetarium_outdoor
plantation_house playground playroom plaza podium_indoor podium_outdoor police_station pond pontoon_bridge poop_deck
porch portico portrait_studio postern power_plant_outdoor print_shop priory promenade promenade_deck pub_indoor
pub_outdoor pulpit putting_green quadrangle quicksand quonset_hut_indoor racecourse raceway raft railroad_track
railway_yard rainforest ramp ranch ranch_house reading_room reception recreation_room rectory recycling_plant_indoor
refectory repair_shop residential_neighborhood resort rest_area restaurant restaurant_kitchen restaurant_patio
restroom_indoor restroom_outdoor revolving_door riding_arena river road_cut rock_arch roller_skating_rink_indoor
roller_skating_rink_outdoor rolling_mill roof roof_garden root_cellar rope_bridge roundabout roundhouse rubble ruin
runway sacristy salt_plain sand_trap sandbar sauna savanna sawmill schoolhouse schoolyard science_museum scriptorium
sea_cliff seawall security_check_point server_room sewer sewing_room shed shipping_room shipyard_outdoor shoe_shop
shopping_mall_indoor shopping_mall_outdoor shower shower_room shrine signal_box sinkhole ski_jump ski_lodge ski_resort
ski_slope sky skywalk_indoor skywalk_outdoor slum snowfield massage_room mineral_bath spillway sporting_goods_store
squash_court stable baseball stadium_outdoor stage_indoor stage_outdoor staircase starting_gate steam_plant_outdoor
steel_mill_indoor storage_room storm_cellar street strip_mall strip_mine student_residence submarine_interior sun_deck
sushi_bar swamp swimming_hole swimming_pool_indoor synagogue_indoor synagogue_outdoor taxistand taxiway tea_garden
tearoom teashop television_room east_asia mesoamerican south_asia western tennis_court_indoor tennis_court_outdoor
tent_outdoor terrace_farm indoor_round indoor_seats theater_outdoor thriftshop throne_room ticket_booth
tobacco_shop_indoor toll_plaza tollbooth topiary_garden tower town_house toyshop track_outdoor trading_floor
trailer_park train_interior train_station_outdoor station tree_farm tree_house trench trestle_bridge tundra rail_indoor
rail_outdoor road_indoor road_outdoor turkish_bath ocean_deep ocean_shallow utility_room valley van_interior
vegetable_garden velodrome_indoor velodrome_outdoor ventilation_shaft veranda vestry veterinarians_office videostore
village vineyard volcano volleyball_court_indoor volleyball_court_outdoor voting_booth waiting_room walk_in_freezer
warehouse_indoor warehouse_outdoor washhouse_indoor washhouse_outdoor watchtower water_mill water_park water_tower
water_treatment_plant_indoor water_treatment_plant_outdoor block cascade cataract fan plunge watering_hole weighbridge
wet_bar wharf wheat_field whispering_gallery widows_walk_interior windmill window_seat barrel_storage winery
witness_stand woodland workroom workshop wrestling_ring_indoor wrestling_ring_outdoor yard youth_hostel zen_garden
ziggurat zoo forklift hollow hutment pueblo vat perfume_shop steel_mill_outdoor orchestra_pit bridle_path lyceum
one-way_street parade_ground pump_room recycling_plant_outdoor chuck_wagon
"""
_SCENE_CATEGORIES = _SCENE_CATEGORIES.strip().split()


class SceneParse150(datasets.GeneratorBasedBuilder):
    """MIT Scene Parsing Benchmark dataset."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="scene_parsing", version=VERSION, description="The scene parsing variant."),
        datasets.BuilderConfig(
            name="instance_segmentation", version=VERSION, description="The instance segmentation variant."
        ),
    ]

    DEFAULT_CONFIG_NAME = "scene_parsing"

    def _info(self):
        if self.config.name == "scene_parsing":
            features = datasets.Features(
                {
                    "image": datasets.Image(),
                    "annotation": datasets.Image(),
                    "scene_category": datasets.ClassLabel(names=_SCENE_CATEGORIES),
                }
            )
        else:
            features = datasets.Features(
                {
                    "image": datasets.Image(),
                    "annotation": datasets.Image(),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        urls = _URLS[self.config.name]

        if self.config.name == "scene_parsing":
            data_dirs = dl_manager.download_and_extract(urls)
            train_data = val_data = os.path.join(data_dirs["train/val"], "ADEChallengeData2016")
            test_data = os.path.join(data_dirs["test"], "release_test")
        else:
            data_dirs = dl_manager.download(urls)
            train_data = dl_manager.iter_archive(data_dirs["images"]), dl_manager.iter_archive(
                data_dirs["annotations"]
            )
            val_data = dl_manager.iter_archive(data_dirs["images"]), dl_manager.iter_archive(data_dirs["annotations"])
            test_data = dl_manager.iter_archive(data_dirs["test"])
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "data": train_data,
                    "split": "training",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"data": test_data, "split": "testing"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "data": val_data,
                    "split": "validation",
                },
            ),
        ]

    def _generate_examples(self, data, split):
        if self.config.name == "scene_parsing":
            if split == "testing":
                image_dir = os.path.join(data, split)
                for idx, image_file in enumerate(os.listdir(image_dir)):
                    yield idx, {
                        "image": os.path.join(image_dir, image_file),
                        "annotation": None,
                        "scene_category": None,
                    }
            else:
                image_id2cat = pd.read_csv(
                    os.path.join(data, "sceneCategories.txt"), sep=" ", names=["image_id", "scene_category"]
                )
                image_id2cat = image_id2cat.set_index("image_id")
                images_dir = os.path.join(data, "images", split)
                annotations_dir = os.path.join(data, "annotations", split)
                for idx, image_file in enumerate(os.listdir(images_dir)):
                    image_id = image_file.split(".")[0]
                    yield idx, {
                        "image": os.path.join(images_dir, image_file),
                        "annotation": os.path.join(annotations_dir, image_id + ".png"),
                        "scene_category": image_id2cat.loc[image_id, "scene_category"],
                    }
        else:
            if split == "testing":
                for idx, (path, file) in enumerate(data):
                    if path.endswith(".jpg"):
                        yield idx, {
                            "image": {"path": path, "bytes": file.read()},
                            "annotation": None,
                        }
            else:
                images, annotations = data
                image_id2annot = {}
                # loads the annotations for the split into RAM (less than 100 MB) to support streaming
                for path_annot, file_annot in annotations:
                    if split in path_annot and path_annot.endswith(".png"):
                        image_id = os.path.basename(path_annot).split(".")[0]
                        image_id2annot[image_id] = (path_annot, file_annot.read())
                for idx, (path_img, file_img) in enumerate(images):
                    if split in path_img and path_img.endswith(".jpg"):
                        image_id = os.path.basename(path_img).split(".")[0]
                        path_annot, bytes_annot = image_id2annot[image_id]
                        yield idx, {
                            "image": {"path": path_img, "bytes": file_img.read()},
                            "annotation": {"path": path_annot, "bytes": bytes_annot},
                        }
