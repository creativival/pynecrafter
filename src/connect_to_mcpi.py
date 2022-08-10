"""src/connect_to_mcpi.py"""
from mcpi.minecraft import Minecraft


class ConnectToMCPI():
    # connection port for MCPI
    PORT_MC = 4711

    # block IDs for MCPI  ## see block.py
    AIR = 0
    STONE = 1
    GRASS_BLOCK = 2
    DIRT = 3
    COBBLESTONE = 4
    OAK_PLANKS = 5
    SAPLING = 6
    BEDROCK = 7
    WATER_FLOWING = 8
    WATER = WATER_FLOWING
    WATER_STATIONARY = 9
    LAVA_FLOWING = 10
    LAVA = LAVA_FLOWING
    LAVA_STATIONARY = 11
    SAND = 12
    GRAVEL = 13
    GOLD_ORE = 14
    IRON_ORE = 15
    COAL_ORE = 16
    OAK_LOG = 17
    OAK_LEAVES = 18
    GLASS = 20
    LAPIS_ORE = 21
    LAPIS_BLOCK = 22
    SANDSTONE = 24
    BED = 26
    RAIL_POWERED = 27
    RAIL_DETECTOR = 28
    COBWEB = 30
    GRASS_TALL = 31
    DEAD_BUSH = 32
    WHITE_WOOL = 35
    ORANGE_WOOL = (35, 1)
    MAGENTA_WOOL = (35, 2)
    LIGHT_BLUE_WOOL = (35, 3)
    YELLOW_WOOL = (35, 4)
    LIME_WOOL = (35, 5)
    PINK_WOOL = (35, 6)
    GRAY_WOOL = (35, 7)
    LIGHT_GRAY_WOOL = (35, 8)
    CYAN_WOOL = (35, 9)
    PURPLE_WOOL = (35, 10)
    BLUE_WOOL = (35, 11)
    BROWN_WOOL = (35, 12)
    GREEN_WOOL = (35, 13)
    RED_WOOL = (35, 14)
    BLACK_WOOL = (35, 15)
    FLOWER_YELLOW = 37
    FLOWER_CYAN = 38
    MUSHROOM_BROWN = 39
    MUSHROOM_RED = 40
    GOLD_BLOCK = 41
    IRON_BLOCK = 42
    STONE_SLAB_DOUBLE = 43
    STONE_SLAB = 44
    BRICK_BLOCK = 45
    TNT = 46
    BOOKSHELF = 47
    MOSS_STONE = 48
    OBSIDIAN = 49
    TORCH = 50
    FIRE = 51
    STAIRS_WOOD = 53
    CHEST = 54
    DIAMOND_ORE = 56
    DIAMOND_BLOCK = 57
    CRAFTING_TABLE = 58
    FARMLAND = 60
    FURNACE = 61
    BURNING_FURNACE = 62
    SIGN_STANDING = 63
    DOOR_WOOD = 64
    LADDER = 65
    RAIL = 66
    STAIRS_COBBLESTONE = 67
    SIGN_WALL = 68
    DOOR_IRON = 71
    REDSTONE_ORE = 73
    TORCH_REDSTONE = 76
    SNOW = 78
    ICE = 79
    SNOW_BLOCK = 80
    CACTUS = 81
    CLAY = 82
    SUGAR_CANE = 83
    FENCE = 85
    PUMPKIN = 86
    NETHERRACK = 87
    SOUL_SAND = 88
    GLOWSTONE_BLOCK = 89
    LIT_PUMPKIN = 91
    STAINED_GLASS = 95
    BEDROCK_INVISIBLE = 95
    TRAPDOOR = 96
    STONE_BRICK = 98
    GLASS_PANE = 102
    MELON = 103
    FENCE_GATE = 107
    STAIRS_BRICK = 108
    STAIRS_STONE_BRICK = 109
    MYCELIUM = 110
    NETHER_BRICK = 112
    FENCE_NETHER_BRICK = 113
    STAIRS_NETHER_BRICK = 114
    END_STONE = 121
    WOODEN_SLAB = 126
    STAIRS_SANDSTONE = 128
    EMERALD_ORE = 129
    RAIL_ACTIVATOR = 157
    LEAVES2 = 161
    TRAPDOOR_IRON = 167
    FENCE_SPRUCE = 188
    FENCE_BIRCH = 189
    FENCE_JUNGLE = 190
    FENCE_DARK_OAK = 191
    FENCE_ACACIA = 192
    DOOR_SPRUCE = 193
    DOOR_BIRCH = 194
    DOOR_JUNGLE = 195
    DOOR_ACACIA = 196
    DOOR_DARK_OAK = 197
    GLOWING_OBSIDIAN = 246
    NETHER_REACTOR_CORE = 247
    PISTON = 33
    JACK_O_LANTERN = 91

    def __init__(self):
        print('connect to mcpi')
        self.mc = Minecraft.create(port=ConnectToMCPI.PORT_MC)
        self.base_position = self.mc.player.getPos()

        self.accept('m', self.transport_blocks_to_mcpi)
        self.accept('n', self.clear_all_blocks)
        # self.accept('p', self.player_set_pos)

    def transport_blocks_to_mcpi(self):
        self.mc.postToChat('transport_blocks_to_mcpi')
        player_position = self.player.position
        self.mc.player.setPos(
            self.base_position.x - player_position.x,
            self.base_position.y + player_position.z,
            self.base_position.z + player_position.y
        )
        for key, block_id in self.block.block_dictionary.items():
            x, y, z = [int(value) for value in key.split('_')]
            block_id_mcpi = self.get(block_id.upper()) or 1
            if isinstance(block_id_mcpi, int):
                self.mc.setBlock(
                    self.base_position.x - x,
                    self.base_position.y + z,
                    self.base_position.z + y,
                    block_id_mcpi
                )
            else:  # colored wool
                self.mc.setBlock(
                    self.base_position.x - x,
                    self.base_position.y + z,
                    self.base_position.z + y,
                    *block_id_mcpi
                )

    def clear_all_blocks(self):
        self.mc.postToChat('clear_all_blocks')
        base_position = self.mc.player.getPos()
        self.mc.setBlocks(
            base_position.x - 100,
            base_position.y,
            base_position.z - 100,
            base_position.x + 100,
            base_position.y + 100,
            base_position.z + 100,
            0  # AIR
        )

        self.mc.setBlocks(
            base_position.x - 100,
            base_position.y - 1,
            base_position.z - 100,
            base_position.x + 100,
            base_position.y - 2,
            base_position.z + 100,
            2  # GRASS
        )


    # def player_set_pos(self):
    #     self.mc.postToChat('player_set_pos')
    #     player_position = self.player.position
    #     player_direction = self.player.direction
    #     self.mc.player.setPos(
    #         self.base_position.x - player_position.x,
    #         self.base_position.y + player_position.z,
    #         self.base_position.z + player_position.y
    #     )
    #     self.mc.player.setDirection(
    #         -player_direction.x,
    #         player_direction.z,
    #         player_direction.y
    #     )
