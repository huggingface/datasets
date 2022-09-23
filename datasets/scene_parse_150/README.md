---
annotations_creators:
- crowdsourced
- expert-generated
language_creators:
- found
language:
- en
license:
- bsd-3-clause
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|ade20k
task_categories:
- image-segmentation
task_ids:
- instance-segmentation
- other-scene-parsing
paperswithcode_id: ade20k
pretty_name: MIT Scene Parsing Benchmark
dataset_info:
- config_name: scene_parsing
  features:
  - name: image
    dtype: image
  - name: annotation
    dtype: image
  - name: scene_category
    dtype:
      class_label:
        names:
          0: airport_terminal
          1: art_gallery
          2: badlands
          3: ball_pit
          4: bathroom
          5: beach
          6: bedroom
          7: booth_indoor
          8: botanical_garden
          9: bridge
          10: bullring
          11: bus_interior
          12: butte
          13: canyon
          14: casino_outdoor
          15: castle
          16: church_outdoor
          17: closet
          18: coast
          19: conference_room
          20: construction_site
          21: corral
          22: corridor
          23: crosswalk
          24: day_care_center
          25: sand
          26: elevator_interior
          27: escalator_indoor
          28: forest_road
          29: gangplank
          30: gas_station
          31: golf_course
          32: gymnasium_indoor
          33: harbor
          34: hayfield
          35: heath
          36: hoodoo
          37: house
          38: hunting_lodge_outdoor
          39: ice_shelf
          40: joss_house
          41: kiosk_indoor
          42: kitchen
          43: landfill
          44: library_indoor
          45: lido_deck_outdoor
          46: living_room
          47: locker_room
          48: market_outdoor
          49: mountain_snowy
          50: office
          51: orchard
          52: arbor
          53: bookshelf
          54: mews
          55: nook
          56: preserve
          57: traffic_island
          58: palace
          59: palace_hall
          60: pantry
          61: patio
          62: phone_booth
          63: establishment
          64: poolroom_home
          65: quonset_hut_outdoor
          66: rice_paddy
          67: sandbox
          68: shopfront
          69: skyscraper
          70: stone_circle
          71: subway_interior
          72: platform
          73: supermarket
          74: swimming_pool_outdoor
          75: television_studio
          76: indoor_procenium
          77: train_railway
          78: coral_reef
          79: viaduct
          80: wave
          81: wind_farm
          82: bottle_storage
          83: abbey
          84: access_road
          85: air_base
          86: airfield
          87: airlock
          88: airplane_cabin
          89: airport
          90: entrance
          91: airport_ticket_counter
          92: alcove
          93: alley
          94: amphitheater
          95: amusement_arcade
          96: amusement_park
          97: anechoic_chamber
          98: apartment_building_outdoor
          99: apse_indoor
          100: apse_outdoor
          101: aquarium
          102: aquatic_theater
          103: aqueduct
          104: arcade
          105: arch
          106: archaelogical_excavation
          107: archive
          108: basketball
          109: football
          110: hockey
          111: performance
          112: rodeo
          113: soccer
          114: armory
          115: army_base
          116: arrival_gate_indoor
          117: arrival_gate_outdoor
          118: art_school
          119: art_studio
          120: artists_loft
          121: assembly_line
          122: athletic_field_indoor
          123: athletic_field_outdoor
          124: atrium_home
          125: atrium_public
          126: attic
          127: auditorium
          128: auto_factory
          129: auto_mechanics_indoor
          130: auto_mechanics_outdoor
          131: auto_racing_paddock
          132: auto_showroom
          133: backstage
          134: backstairs
          135: badminton_court_indoor
          136: badminton_court_outdoor
          137: baggage_claim
          138: shop
          139: exterior
          140: balcony_interior
          141: ballroom
          142: bamboo_forest
          143: bank_indoor
          144: bank_outdoor
          145: bank_vault
          146: banquet_hall
          147: baptistry_indoor
          148: baptistry_outdoor
          149: bar
          150: barbershop
          151: barn
          152: barndoor
          153: barnyard
          154: barrack
          155: baseball_field
          156: basement
          157: basilica
          158: basketball_court_indoor
          159: basketball_court_outdoor
          160: bathhouse
          161: batters_box
          162: batting_cage_indoor
          163: batting_cage_outdoor
          164: battlement
          165: bayou
          166: bazaar_indoor
          167: bazaar_outdoor
          168: beach_house
          169: beauty_salon
          170: bedchamber
          171: beer_garden
          172: beer_hall
          173: belfry
          174: bell_foundry
          175: berth
          176: berth_deck
          177: betting_shop
          178: bicycle_racks
          179: bindery
          180: biology_laboratory
          181: bistro_indoor
          182: bistro_outdoor
          183: bleachers_indoor
          184: bleachers_outdoor
          185: boardwalk
          186: boat_deck
          187: boathouse
          188: bog
          189: bomb_shelter_indoor
          190: bookbindery
          191: bookstore
          192: bow_window_indoor
          193: bow_window_outdoor
          194: bowling_alley
          195: box_seat
          196: boxing_ring
          197: breakroom
          198: brewery_indoor
          199: brewery_outdoor
          200: brickyard_indoor
          201: brickyard_outdoor
          202: building_complex
          203: building_facade
          204: bullpen
          205: burial_chamber
          206: bus_depot_indoor
          207: bus_depot_outdoor
          208: bus_shelter
          209: bus_station_indoor
          210: bus_station_outdoor
          211: butchers_shop
          212: cabana
          213: cabin_indoor
          214: cabin_outdoor
          215: cafeteria
          216: call_center
          217: campsite
          218: campus
          219: natural
          220: urban
          221: candy_store
          222: canteen
          223: car_dealership
          224: backseat
          225: frontseat
          226: caravansary
          227: cardroom
          228: cargo_container_interior
          229: airplane
          230: boat
          231: freestanding
          232: carport_indoor
          233: carport_outdoor
          234: carrousel
          235: casino_indoor
          236: catacomb
          237: cathedral_indoor
          238: cathedral_outdoor
          239: catwalk
          240: cavern_indoor
          241: cavern_outdoor
          242: cemetery
          243: chalet
          244: chaparral
          245: chapel
          246: checkout_counter
          247: cheese_factory
          248: chemical_plant
          249: chemistry_lab
          250: chicken_coop_indoor
          251: chicken_coop_outdoor
          252: chicken_farm_indoor
          253: chicken_farm_outdoor
          254: childs_room
          255: choir_loft_interior
          256: church_indoor
          257: circus_tent_indoor
          258: circus_tent_outdoor
          259: city
          260: classroom
          261: clean_room
          262: cliff
          263: booth
          264: room
          265: clock_tower_indoor
          266: cloister_indoor
          267: cloister_outdoor
          268: clothing_store
          269: coast_road
          270: cockpit
          271: coffee_shop
          272: computer_room
          273: conference_center
          274: conference_hall
          275: confessional
          276: control_room
          277: control_tower_indoor
          278: control_tower_outdoor
          279: convenience_store_indoor
          280: convenience_store_outdoor
          281: corn_field
          282: cottage
          283: cottage_garden
          284: courthouse
          285: courtroom
          286: courtyard
          287: covered_bridge_interior
          288: crawl_space
          289: creek
          290: crevasse
          291: library
          292: cybercafe
          293: dacha
          294: dairy_indoor
          295: dairy_outdoor
          296: dam
          297: dance_school
          298: darkroom
          299: delicatessen
          300: dentists_office
          301: department_store
          302: departure_lounge
          303: vegetation
          304: desert_road
          305: diner_indoor
          306: diner_outdoor
          307: dinette_home
          308: vehicle
          309: dining_car
          310: dining_hall
          311: dining_room
          312: dirt_track
          313: discotheque
          314: distillery
          315: ditch
          316: dock
          317: dolmen
          318: donjon
          319: doorway_indoor
          320: doorway_outdoor
          321: dorm_room
          322: downtown
          323: drainage_ditch
          324: dress_shop
          325: dressing_room
          326: drill_rig
          327: driveway
          328: driving_range_indoor
          329: driving_range_outdoor
          330: drugstore
          331: dry_dock
          332: dugout
          333: earth_fissure
          334: editing_room
          335: electrical_substation
          336: elevated_catwalk
          337: door
          338: freight_elevator
          339: elevator_lobby
          340: elevator_shaft
          341: embankment
          342: embassy
          343: engine_room
          344: entrance_hall
          345: escalator_outdoor
          346: escarpment
          347: estuary
          348: excavation
          349: exhibition_hall
          350: fabric_store
          351: factory_indoor
          352: factory_outdoor
          353: fairway
          354: farm
          355: fastfood_restaurant
          356: fence
          357: cargo_deck
          358: ferryboat_indoor
          359: passenger_deck
          360: cultivated
          361: wild
          362: field_road
          363: fire_escape
          364: fire_station
          365: firing_range_indoor
          366: firing_range_outdoor
          367: fish_farm
          368: fishmarket
          369: fishpond
          370: fitting_room_interior
          371: fjord
          372: flea_market_indoor
          373: flea_market_outdoor
          374: floating_dry_dock
          375: flood
          376: florist_shop_indoor
          377: florist_shop_outdoor
          378: fly_bridge
          379: food_court
          380: football_field
          381: broadleaf
          382: needleleaf
          383: forest_fire
          384: forest_path
          385: formal_garden
          386: fort
          387: fortress
          388: foundry_indoor
          389: foundry_outdoor
          390: fountain
          391: freeway
          392: funeral_chapel
          393: funeral_home
          394: furnace_room
          395: galley
          396: game_room
          397: garage_indoor
          398: garage_outdoor
          399: garbage_dump
          400: gasworks
          401: gate
          402: gatehouse
          403: gazebo_interior
          404: general_store_indoor
          405: general_store_outdoor
          406: geodesic_dome_indoor
          407: geodesic_dome_outdoor
          408: ghost_town
          409: gift_shop
          410: glacier
          411: glade
          412: gorge
          413: granary
          414: great_hall
          415: greengrocery
          416: greenhouse_indoor
          417: greenhouse_outdoor
          418: grotto
          419: guardhouse
          420: gulch
          421: gun_deck_indoor
          422: gun_deck_outdoor
          423: gun_store
          424: hacienda
          425: hallway
          426: handball_court
          427: hangar_indoor
          428: hangar_outdoor
          429: hardware_store
          430: hat_shop
          431: hatchery
          432: hayloft
          433: hearth
          434: hedge_maze
          435: hedgerow
          436: heliport
          437: herb_garden
          438: highway
          439: hill
          440: home_office
          441: home_theater
          442: hospital
          443: hospital_room
          444: hot_spring
          445: hot_tub_indoor
          446: hot_tub_outdoor
          447: hotel_outdoor
          448: hotel_breakfast_area
          449: hotel_room
          450: hunting_lodge_indoor
          451: hut
          452: ice_cream_parlor
          453: ice_floe
          454: ice_skating_rink_indoor
          455: ice_skating_rink_outdoor
          456: iceberg
          457: igloo
          458: imaret
          459: incinerator_indoor
          460: incinerator_outdoor
          461: industrial_area
          462: industrial_park
          463: inn_indoor
          464: inn_outdoor
          465: irrigation_ditch
          466: islet
          467: jacuzzi_indoor
          468: jacuzzi_outdoor
          469: jail_indoor
          470: jail_outdoor
          471: jail_cell
          472: japanese_garden
          473: jetty
          474: jewelry_shop
          475: junk_pile
          476: junkyard
          477: jury_box
          478: kasbah
          479: kennel_indoor
          480: kennel_outdoor
          481: kindergarden_classroom
          482: kiosk_outdoor
          483: kitchenette
          484: lab_classroom
          485: labyrinth_indoor
          486: labyrinth_outdoor
          487: lagoon
          488: artificial
          489: landing
          490: landing_deck
          491: laundromat
          492: lava_flow
          493: lavatory
          494: lawn
          495: lean-to
          496: lecture_room
          497: legislative_chamber
          498: levee
          499: library_outdoor
          500: lido_deck_indoor
          501: lift_bridge
          502: lighthouse
          503: limousine_interior
          504: liquor_store_indoor
          505: liquor_store_outdoor
          506: loading_dock
          507: lobby
          508: lock_chamber
          509: loft
          510: lookout_station_indoor
          511: lookout_station_outdoor
          512: lumberyard_indoor
          513: lumberyard_outdoor
          514: machine_shop
          515: manhole
          516: mansion
          517: manufactured_home
          518: market_indoor
          519: marsh
          520: martial_arts_gym
          521: mastaba
          522: maternity_ward
          523: mausoleum
          524: medina
          525: menhir
          526: mesa
          527: mess_hall
          528: mezzanine
          529: military_hospital
          530: military_hut
          531: military_tent
          532: mine
          533: mineshaft
          534: mini_golf_course_indoor
          535: mini_golf_course_outdoor
          536: mission
          537: dry
          538: water
          539: mobile_home
          540: monastery_indoor
          541: monastery_outdoor
          542: moon_bounce
          543: moor
          544: morgue
          545: mosque_indoor
          546: mosque_outdoor
          547: motel
          548: mountain
          549: mountain_path
          550: mountain_road
          551: movie_theater_indoor
          552: movie_theater_outdoor
          553: mudflat
          554: museum_indoor
          555: museum_outdoor
          556: music_store
          557: music_studio
          558: misc
          559: natural_history_museum
          560: naval_base
          561: newsroom
          562: newsstand_indoor
          563: newsstand_outdoor
          564: nightclub
          565: nuclear_power_plant_indoor
          566: nuclear_power_plant_outdoor
          567: nunnery
          568: nursery
          569: nursing_home
          570: oasis
          571: oast_house
          572: observatory_indoor
          573: observatory_outdoor
          574: observatory_post
          575: ocean
          576: office_building
          577: office_cubicles
          578: oil_refinery_indoor
          579: oil_refinery_outdoor
          580: oilrig
          581: operating_room
          582: optician
          583: organ_loft_interior
          584: orlop_deck
          585: ossuary
          586: outcropping
          587: outhouse_indoor
          588: outhouse_outdoor
          589: overpass
          590: oyster_bar
          591: oyster_farm
          592: acropolis
          593: aircraft_carrier_object
          594: amphitheater_indoor
          595: archipelago
          596: questionable
          597: assembly_hall
          598: assembly_plant
          599: awning_deck
          600: back_porch
          601: backdrop
          602: backroom
          603: backstage_outdoor
          604: backstairs_indoor
          605: backwoods
          606: ballet
          607: balustrade
          608: barbeque
          609: basin_outdoor
          610: bath_indoor
          611: bath_outdoor
          612: bathhouse_outdoor
          613: battlefield
          614: bay
          615: booth_outdoor
          616: bottomland
          617: breakfast_table
          618: bric-a-brac
          619: brooklet
          620: bubble_chamber
          621: buffet
          622: bulkhead
          623: bunk_bed
          624: bypass
          625: byroad
          626: cabin_cruiser
          627: cargo_helicopter
          628: cellar
          629: chair_lift
          630: cocktail_lounge
          631: corner
          632: country_house
          633: country_road
          634: customhouse
          635: dance_floor
          636: deck-house_boat_deck_house
          637: deck-house_deck_house
          638: dining_area
          639: diving_board
          640: embrasure
          641: entranceway_indoor
          642: entranceway_outdoor
          643: entryway_outdoor
          644: estaminet
          645: farm_building
          646: farmhouse
          647: feed_bunk
          648: field_house
          649: field_tent_indoor
          650: field_tent_outdoor
          651: fire_trench
          652: fireplace
          653: flashflood
          654: flatlet
          655: floating_dock
          656: flood_plain
          657: flowerbed
          658: flume_indoor
          659: flying_buttress
          660: foothill
          661: forecourt
          662: foreshore
          663: front_porch
          664: garden
          665: gas_well
          666: glen
          667: grape_arbor
          668: grove
          669: guardroom
          670: guesthouse
          671: gymnasium_outdoor
          672: head_shop
          673: hen_yard
          674: hillock
          675: housing_estate
          676: housing_project
          677: howdah
          678: inlet
          679: insane_asylum
          680: outside
          681: juke_joint
          682: jungle
          683: kraal
          684: laboratorywet
          685: landing_strip
          686: layby
          687: lean-to_tent
          688: loge
          689: loggia_outdoor
          690: lower_deck
          691: luggage_van
          692: mansard
          693: meadow
          694: meat_house
          695: megalith
          696: mens_store_outdoor
          697: mental_institution_indoor
          698: mental_institution_outdoor
          699: military_headquarters
          700: millpond
          701: millrace
          702: natural_spring
          703: nursing_home_outdoor
          704: observation_station
          705: open-hearth_furnace
          706: operating_table
          707: outbuilding
          708: palestra
          709: parkway
          710: patio_indoor
          711: pavement
          712: pawnshop_outdoor
          713: pinetum
          714: piste_road
          715: pizzeria_outdoor
          716: powder_room
          717: pumping_station
          718: reception_room
          719: rest_stop
          720: retaining_wall
          721: rift_valley
          722: road
          723: rock_garden
          724: rotisserie
          725: safari_park
          726: salon
          727: saloon
          728: sanatorium
          729: science_laboratory
          730: scrubland
          731: scullery
          732: seaside
          733: semidesert
          734: shelter
          735: shelter_deck
          736: shelter_tent
          737: shore
          738: shrubbery
          739: sidewalk
          740: snack_bar
          741: snowbank
          742: stage_set
          743: stall
          744: stateroom
          745: store
          746: streetcar_track
          747: student_center
          748: study_hall
          749: sugar_refinery
          750: sunroom
          751: supply_chamber
          752: t-bar_lift
          753: tannery
          754: teahouse
          755: threshing_floor
          756: ticket_window_indoor
          757: tidal_basin
          758: tidal_river
          759: tiltyard
          760: tollgate
          761: tomb
          762: tract_housing
          763: trellis
          764: truck_stop
          765: upper_balcony
          766: vestibule
          767: vinery
          768: walkway
          769: war_room
          770: washroom
          771: water_fountain
          772: water_gate
          773: waterscape
          774: waterway
          775: wetland
          776: widows_walk_indoor
          777: windstorm
          778: packaging_plant
          779: pagoda
          780: paper_mill
          781: park
          782: parking_garage_indoor
          783: parking_garage_outdoor
          784: parking_lot
          785: parlor
          786: particle_accelerator
          787: party_tent_indoor
          788: party_tent_outdoor
          789: pasture
          790: pavilion
          791: pawnshop
          792: pedestrian_overpass_indoor
          793: penalty_box
          794: pet_shop
          795: pharmacy
          796: physics_laboratory
          797: piano_store
          798: picnic_area
          799: pier
          800: pig_farm
          801: pilothouse_indoor
          802: pilothouse_outdoor
          803: pitchers_mound
          804: pizzeria
          805: planetarium_indoor
          806: planetarium_outdoor
          807: plantation_house
          808: playground
          809: playroom
          810: plaza
          811: podium_indoor
          812: podium_outdoor
          813: police_station
          814: pond
          815: pontoon_bridge
          816: poop_deck
          817: porch
          818: portico
          819: portrait_studio
          820: postern
          821: power_plant_outdoor
          822: print_shop
          823: priory
          824: promenade
          825: promenade_deck
          826: pub_indoor
          827: pub_outdoor
          828: pulpit
          829: putting_green
          830: quadrangle
          831: quicksand
          832: quonset_hut_indoor
          833: racecourse
          834: raceway
          835: raft
          836: railroad_track
          837: railway_yard
          838: rainforest
          839: ramp
          840: ranch
          841: ranch_house
          842: reading_room
          843: reception
          844: recreation_room
          845: rectory
          846: recycling_plant_indoor
          847: refectory
          848: repair_shop
          849: residential_neighborhood
          850: resort
          851: rest_area
          852: restaurant
          853: restaurant_kitchen
          854: restaurant_patio
          855: restroom_indoor
          856: restroom_outdoor
          857: revolving_door
          858: riding_arena
          859: river
          860: road_cut
          861: rock_arch
          862: roller_skating_rink_indoor
          863: roller_skating_rink_outdoor
          864: rolling_mill
          865: roof
          866: roof_garden
          867: root_cellar
          868: rope_bridge
          869: roundabout
          870: roundhouse
          871: rubble
          872: ruin
          873: runway
          874: sacristy
          875: salt_plain
          876: sand_trap
          877: sandbar
          878: sauna
          879: savanna
          880: sawmill
          881: schoolhouse
          882: schoolyard
          883: science_museum
          884: scriptorium
          885: sea_cliff
          886: seawall
          887: security_check_point
          888: server_room
          889: sewer
          890: sewing_room
          891: shed
          892: shipping_room
          893: shipyard_outdoor
          894: shoe_shop
          895: shopping_mall_indoor
          896: shopping_mall_outdoor
          897: shower
          898: shower_room
          899: shrine
          900: signal_box
          901: sinkhole
          902: ski_jump
          903: ski_lodge
          904: ski_resort
          905: ski_slope
          906: sky
          907: skywalk_indoor
          908: skywalk_outdoor
          909: slum
          910: snowfield
          911: massage_room
          912: mineral_bath
          913: spillway
          914: sporting_goods_store
          915: squash_court
          916: stable
          917: baseball
          918: stadium_outdoor
          919: stage_indoor
          920: stage_outdoor
          921: staircase
          922: starting_gate
          923: steam_plant_outdoor
          924: steel_mill_indoor
          925: storage_room
          926: storm_cellar
          927: street
          928: strip_mall
          929: strip_mine
          930: student_residence
          931: submarine_interior
          932: sun_deck
          933: sushi_bar
          934: swamp
          935: swimming_hole
          936: swimming_pool_indoor
          937: synagogue_indoor
          938: synagogue_outdoor
          939: taxistand
          940: taxiway
          941: tea_garden
          942: tearoom
          943: teashop
          944: television_room
          945: east_asia
          946: mesoamerican
          947: south_asia
          948: western
          949: tennis_court_indoor
          950: tennis_court_outdoor
          951: tent_outdoor
          952: terrace_farm
          953: indoor_round
          954: indoor_seats
          955: theater_outdoor
          956: thriftshop
          957: throne_room
          958: ticket_booth
          959: tobacco_shop_indoor
          960: toll_plaza
          961: tollbooth
          962: topiary_garden
          963: tower
          964: town_house
          965: toyshop
          966: track_outdoor
          967: trading_floor
          968: trailer_park
          969: train_interior
          970: train_station_outdoor
          971: station
          972: tree_farm
          973: tree_house
          974: trench
          975: trestle_bridge
          976: tundra
          977: rail_indoor
          978: rail_outdoor
          979: road_indoor
          980: road_outdoor
          981: turkish_bath
          982: ocean_deep
          983: ocean_shallow
          984: utility_room
          985: valley
          986: van_interior
          987: vegetable_garden
          988: velodrome_indoor
          989: velodrome_outdoor
          990: ventilation_shaft
          991: veranda
          992: vestry
          993: veterinarians_office
          994: videostore
          995: village
          996: vineyard
          997: volcano
          998: volleyball_court_indoor
          999: volleyball_court_outdoor
          1000: voting_booth
          1001: waiting_room
          1002: walk_in_freezer
          1003: warehouse_indoor
          1004: warehouse_outdoor
          1005: washhouse_indoor
          1006: washhouse_outdoor
          1007: watchtower
          1008: water_mill
          1009: water_park
          1010: water_tower
          1011: water_treatment_plant_indoor
          1012: water_treatment_plant_outdoor
          1013: block
          1014: cascade
          1015: cataract
          1016: fan
          1017: plunge
          1018: watering_hole
          1019: weighbridge
          1020: wet_bar
          1021: wharf
          1022: wheat_field
          1023: whispering_gallery
          1024: widows_walk_interior
          1025: windmill
          1026: window_seat
          1027: barrel_storage
          1028: winery
          1029: witness_stand
          1030: woodland
          1031: workroom
          1032: workshop
          1033: wrestling_ring_indoor
          1034: wrestling_ring_outdoor
          1035: yard
          1036: youth_hostel
          1037: zen_garden
          1038: ziggurat
          1039: zoo
          1040: forklift
          1041: hollow
          1042: hutment
          1043: pueblo
          1044: vat
          1045: perfume_shop
          1046: steel_mill_outdoor
          1047: orchestra_pit
          1048: bridle_path
          1049: lyceum
          1050: one-way_street
          1051: parade_ground
          1052: pump_room
          1053: recycling_plant_outdoor
          1054: chuck_wagon
  splits:
  - name: test
    num_bytes: 744607
    num_examples: 3352
  - name: train
    num_bytes: 8468086
    num_examples: 20210
  - name: validation
    num_bytes: 838032
    num_examples: 2000
  download_size: 1179202534
  dataset_size: 10050725
- config_name: instance_segmentation
  features:
  - name: image
    dtype: image
  - name: annotation
    dtype: image
  splits:
  - name: test
    num_bytes: 212493928
    num_examples: 3352
  - name: train
    num_bytes: 862611544
    num_examples: 20210
  - name: validation
    num_bytes: 87502294
    num_examples: 2000
  download_size: 1197393920
  dataset_size: 1162607766
---

# Dataset Card for MIT Scene Parsing Benchmark

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Annotations](#annotations)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Social Impact of Dataset](#social-impact-of-dataset)
  - [Discussion of Biases](#discussion-of-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** [MIT Scene Parsing Benchmark homepage](http://sceneparsing.csail.mit.edu/)
- **Repository:** [Scene Parsing repository (Caffe/Torch7)](https://github.com/CSAILVision/sceneparsing),[Scene Parsing repository (PyTorch)](https://github.com/CSAILVision/semantic-segmentation-pytorch) and [Instance Segmentation repository](https://github.com/CSAILVision/placeschallenge/tree/master/instancesegmentation)
- **Paper:** [Scene Parsing through ADE20K Dataset](http://people.csail.mit.edu/bzhou/publication/scene-parse-camera-ready.pdf) and [Semantic Understanding of Scenes through ADE20K Dataset](https://arxiv.org/abs/1608.05442)
- **Leaderboard:** [MIT Scene Parsing Benchmark leaderboard](http://sceneparsing.csail.mit.edu/#:~:text=twice%20per%20week.-,leaderboard,-Organizers)
- **Point of Contact:** [Bolei Zhou](mailto:bzhou@ie.cuhk.edu.hk)

### Dataset Summary

Scene parsing is the task of segmenting and parsing an image into different image regions associated with semantic categories, such as sky, road, person, and bed. MIT Scene Parsing Benchmark (SceneParse150) provides a standard training and evaluation platform for the algorithms of scene parsing. The data for this benchmark comes from ADE20K Dataset which contains more than 20K scene-centric images exhaustively annotated with objects and object parts. Specifically, the benchmark is divided into 20K images for training, 2K images for validation, and another batch of held-out images for testing. There are in total 150 semantic categories included for evaluation, which include e.g. sky, road, grass, and discrete objects like person, car, bed. Note that there are non-uniform distribution of objects occuring in the images, mimicking a more natural object occurrence in daily scene.

The goal of this benchmark is to segment and parse an image into different image regions associated with semantic categories, such as sky, road, person, and bedThis benchamark is similar to semantic segmentation tasks in COCO and Pascal Dataset, but the data is more scene-centric and with a diverse range of object categories. The data for this benchmark comes from ADE20K Dataset which contains more than 20K scene-centric images exhaustively annotated with objects and object parts.

### Supported Tasks and Leaderboards

- `scene-parsing`: The goal of this task is to segment the whole image densely into semantic classes (image regions), where each pixel is assigned a class label such as the region of *tree* and the region of *building*.
[The leaderboard](http://sceneparsing.csail.mit.edu/#:~:text=twice%20per%20week.-,leaderboard,-Organizers) for this task ranks the models by considering the mean of the pixel-wise accuracy and class-wise IoU as the final score. Pixel-wise accuracy indicates the ratio of pixels which are correctly predicted, while class-wise IoU indicates the Intersection of Union of pixels averaged over all the 150 semantic categories. Refer to the [Development Kit](https://github.com/CSAILVision/sceneparsing) for the detail.

- `instance-segmentation`: The goal of this task is to detect the object instances inside an image and further generate the precise segmentation masks of the objects. Its difference compared to the task of scene parsing is that in scene parsing there is no instance concept for the segmented regions, instead in instance segmentation if there are three persons in the scene, the network is required to segment each one of the person regions. This task doesn't have an active leaderboard. The performance of the instance segmentation algorithms is evaluated by Average Precision (AP, or mAP), following COCO evaluation metrics. For each image, at most 255 top-scoring instance masks are taken across all categories. Each instance mask prediction is only considered if its IoU with ground truth is above a certain threshold. There are 10 IoU thresholds of 0.50:0.05:0.95 for evaluation. The final AP is averaged across 10 IoU thresholds and 100 categories. You can refer to COCO evaluation page for more explanation: http://mscoco.org/dataset/#detections-eval

### Languages

English.

## Dataset Structure

### Data Instances

A data point comprises an image and its annotation mask, which is `None` in the testing set. The `scene_parsing` configuration has an additional `scene_category` field.

#### `scene_parsing`

```
{
  'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=683x512 at 0x1FF32A3EDA0>,
  'annotation': <PIL.PngImagePlugin.PngImageFile image mode=L size=683x512 at 0x1FF32E5B978>,
  'scene_category': 0
}
```

#### `instance_segmentation`

```
{
  'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=256x256 at 0x20B51B5C400>,
  'annotation': <PIL.PngImagePlugin.PngImageFile image mode=RGB size=256x256 at 0x20B57051B38>
}
```

### Data Fields

#### `scene_parsing`

- `image`: A `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`.
- `annotation`: A `PIL.Image.Image` object containing the annotation mask.
- `scene_category`: A scene category for the image (e.g. `airport_terminal`, `canyon`, `mobile_home`).

> **Note**: annotation masks contain labels ranging from 0 to 150, where 0 refers to "other objects". Those pixels are not considered in the official evaluation. Refer to [this file](https://github.com/CSAILVision/sceneparsing/blob/master/objectInfo150.csv) for the information about the labels of the 150 semantic categories, including indices, pixel ratios and names.

#### `instance_segmentation`

- `image`: A `PIL.Image.Image` object containing the image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`.
- `annotation`: A `PIL.Image.Image` object containing the annotation mask.

> **Note**: in the instance annotation masks, the R(ed) channel encodes category ID, and the G(reen) channel encodes instance ID. Each object instance has a unique instance ID regardless of its category ID. In the dataset, all images have <256 object instances. Refer to [this file (train split)](https://github.com/CSAILVision/placeschallenge/blob/master/instancesegmentation/instanceInfo100_train.txt) and to [this file (validation split)](https://github.com/CSAILVision/placeschallenge/blob/master/instancesegmentation/instanceInfo100_val.txt) for the information about the labels of the 100 semantic categories. To find the mapping between the semantic categories for `instance_segmentation` and `scene_parsing`, refer to [this file](https://github.com/CSAILVision/placeschallenge/blob/master/instancesegmentation/categoryMapping.txt).

### Data Splits

The data is split into training, test and validation set. The training data contains 20210 images, the testing data contains 3352 images and the validation data contains 2000 images.

## Dataset Creation

### Curation Rationale

The rationale from the paper for the ADE20K dataset from which this benchmark originates:

> Semantic understanding of visual scenes is one of the holy grails of computer vision. Despite efforts of the community in data collection, there are still few image datasets covering a wide range of scenes and object categories with pixel-wise annotations for scene understanding. In this work, we present a densely annotated dataset ADE20K, which spans diverse annotations of scenes, objects, parts of objects, and
in some cases even parts of parts.

> The motivation of this work is to collect a dataset that has densely annotated images (every pixel has a semantic label) with a large and an unrestricted open vocabulary. The
images in our dataset are manually segmented in great detail, covering a diverse set of scenes, object and object part categories. The challenge for collecting such annotations is finding reliable annotators, as well as the fact that labeling is difficult if the class list is not defined in advance. On the other hand, open vocabulary naming also suffers from naming inconsistencies across different annotators. In contrast,
our dataset was annotated by a single expert annotator, providing extremely detailed and exhaustive image annotations. On average, our annotator labeled 29 annotation segments per image, compared to the 16 segments per image labeled by external annotators (like workers from Amazon Mechanical Turk). Furthermore, the data consistency and quality are much higher than that of external annotators.

### Source Data

#### Initial Data Collection and Normalization

Images come from the LabelMe, SUN datasets, and Places and were selected to cover the 900 scene categories defined in the SUN database.

This benchmark was built by selecting the top 150 objects ranked by their total pixel ratios from the ADE20K dataset. As the original images in the ADE20K dataset have various sizes, for simplicity those large-sized images were rescaled to make their minimum heights or widths as 512. Among the 150 objects, there are 35 stuff classes (i.e., wall, sky, road) and 115 discrete objects (i.e., car, person, table). The annotated pixels of the 150 objects occupy 92.75% of all the pixels in the dataset, where the stuff classes occupy 60.92%, and discrete objects occupy 31.83%.

#### Who are the source language producers?

The same as in the LabelMe, SUN datasets, and Places datasets.

### Annotations

#### Annotation process

Annotation process for the ADE20K dataset:

> **Image Annotation.** For our dataset, we are interested in having a diverse set of scenes with dense annotations of all the objects present. Images come from the LabelMe, SUN datasets, and Places and were selected to cover the 900 scene categories defined in the SUN database. Images were annotated by a single expert worker using the LabelMe interface. Fig. 2 shows a snapshot of the annotation interface and one fully segmented image. The worker provided three types of annotations: object segments with names, object parts, and attributes. All object instances are segmented independently so that the dataset could be used to train and evaluate detection or segmentation algorithms. Datasets such as COCO, Pascal or Cityscape start by defining a set of object categories of interest. However, when labeling all the objects in a scene, working with a predefined list of objects is not possible as new categories
appear frequently (see fig. 5.d). Here, the annotator created a dictionary of visual concepts where new classes were added constantly to ensure consistency in object naming. Object parts are associated with object instances. Note that parts can have parts too, and we label these associations as well. For example, the ‘rim’ is a part of a ‘wheel’, which in turn is part of a ‘car’. A ‘knob’ is a part of a ‘door’
that can be part of a ‘cabinet’. The total part hierarchy has a depth of 3. The object and part hierarchy is in the supplementary materials.

> **Annotation Consistency.** Defining a labeling protocol is relatively easy when the labeling task is restricted to a fixed list of object classes, however it becomes challenging when the class list is openended. As the goal is to label all the objects within each image, the list of classes grows unbounded. >Many object classes appear only a few times across the entire collection of images. However, those rare >object classes cannot be ignored as they might be important elements for the interpretation of the scene. >Labeling in these conditions becomes difficult because we need to keep a growing list of all the object >classes in order to have a consistent naming across the entire dataset. Despite the annotator’s best effort, >the process is not free of noise. To analyze the annotation consistency we took a subset of 61 randomly >chosen images from the validation set, then asked our annotator to annotate them again (there is a time difference of six months). One expects that there are some differences between the two annotations. A few examples are shown in Fig 3. On average, 82.4% of the pixels got the same label. The remaining 17.6% of pixels had some errors for which we grouped into three error types as follows:
>
>    • Segmentation quality: Variations in the quality of segmentation and outlining of the object boundary.  One typical source of error arises when segmenting complex objects such as buildings and trees, which can be segmented with different degrees of precision. 5.7% of the pixels had this type of error.
>
>    • Object naming: Differences in object naming (due to ambiguity or similarity between concepts, for instance calling a big car a ‘car’ in one segmentation and a ‘truck’ in the another one, or a ‘palm tree’ a‘tree’. 6.0% of the pixels had naming issues. These errors can be reduced by defining a very precise terminology, but this becomes much harder with a large growing vocabulary.
>
>    • Segmentation quantity: Missing objects in one of the two segmentations. There is a very large number of objects in each image and some images might be annotated more thoroughly than others. For example, in the third column of Fig 3 the annotator missed some small objects in different annotations. 5.9% of the pixels are due to missing labels. A similar issue existed in segmentation datasets such as the Berkeley Image segmentation dataset.
>
> The median error values for the three error types are: 4.8%, 0.3% and 2.6% showing that the mean value is dominated by a few images, and that the most common type of error is segmentation quality.
To further compare the annotation done by our single expert annotator and the AMT-like annotators, 20 images
from the validation set are annotated by two invited external annotators, both with prior experience in image labeling. The first external annotator had 58.5% of inconsistent pixels compared to the segmentation provided by our annotator, and the second external annotator had 75% of the inconsistent pixels. Many of these inconsistencies are due to the poor quality of the segmentations provided by external annotators (as it has been observed with AMT which requires multiple verification steps for quality control). For the
best external annotator (the first one), 7.9% of pixels have inconsistent segmentations (just slightly worse than our annotator), 14.9% have inconsistent object naming and 35.8% of the pixels correspond to missing objects, which is due to the much smaller number of objects annotated by the external annotator in comparison with the ones annotated by our expert annotator. The external annotators labeled on average 16 segments per image while our annotator provided 29 segments per image.

#### Who are the annotators?

Three expert annotators and the AMT-like annotators.

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

Refer to the `Annotation Consistency` subsection of `Annotation Process`.

## Additional Information

### Dataset Curators

Bolei Zhou, Hang Zhao, Xavier Puig, Sanja Fidler, Adela Barriuso and Antonio Torralba.

### Licensing Information

The MIT Scene Parsing Benchmark dataset is licensed under a [BSD 3-Clause License](https://github.com/CSAILVision/sceneparsing/blob/master/LICENSE).

### Citation Information

```bibtex
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
```

### Contributions

Thanks to [@mariosasko](https://github.com/mariosasko) for adding this dataset.