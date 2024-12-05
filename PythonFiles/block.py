class Block:
    def __init__(self, removed_pixel, game_map, is_question_block):
        self.remove_pixel = removed_pixel
        self.breaked = False
        self.is_question_block = is_question_block
        self.game_map = game_map


    def block_hitted(self):
        if self.is_question_block:
          pixel_line = self.get_question_block_pixels()
        else:
          pixel_line = self.get_block_pixels()

        if len(pixel_line) == 0:
            return

        pixel_line.sort(key=lambda pixel: pixel.x)

        median_point = ((pixel_line[0].x + pixel_line[-1].x) // 2 , pixel_line[0].y)
       
        block_center = None

        for floor in self.game_map.floor:
            if floor.x == median_point[0] and floor.y < median_point[1]:
                self.game_map.floor.remove(floor)

                block_center = floor.x, (floor.y + median_point[1]) // 2
                break

        if block_center:
            self.break_block(block_center)


    def get_question_block_pixels(self):
        pixel_line = []

        self.game_map.question_marks.remove(self.remove_pixel)

        for pixel_block in self.game_map.question_marks:
            if self.remove_pixel.y == pixel_block.y:
                pixel_line.append(pixel_block)
                self.game_map.question_marks.remove(pixel_block)
                self.game_map.map_image.set_at((pixel_block.x, pixel_block.y), (0, 162, 232)) 

        return pixel_line
    

    def get_block_pixels(self):
      
        pixel_line = []

        self.game_map.blocks.remove(self.remove_pixel)

        for pixel_block in self.game_map.question_marks:
            if self.remove_pixel.y == pixel_block.y:
                pixel_line.append(pixel_block)
                self.game_map.blocks.remove(self.remove_pixel)

                self.game_map.map_image.set_at((pixel_block.x, pixel_block.y), (0, 162, 232)) 

        return pixel_line
       

    def break_block(self, block_center):  
        self.breaked = True

        area_width = 17 
        area_height = 17 
  
        x_limits = (round(block_center[0] - area_width / 2), round(block_center[0] + area_width / 2))
        y_limits = (round(block_center[1] - area_height / 2), round(block_center[1] + area_height / 2))

        for y in range(y_limits[0], y_limits[1]):
            for x in range(x_limits[0], x_limits[1]):
                    
                # Switches the pixels colors of the block for the sky color
                self.game_map.map_image.set_at((x, y), (0, 162, 232))  
                    
                # Remove the block from the other colliders
                self.game_map.question_marks[:] = [block for block in self.game_map.question_marks if not (block.x == x and block.y == y)]
                self.game_map.floor[:] = [floor for floor in self.game_map.floor if not (floor.x == x and floor.y == y)]
     