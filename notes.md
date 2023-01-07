# platformer

LU


THIRD VIDEO
https://www.youtube.com/watch?v=IUe2pdTWroc&t=0s
6:52
13 55 w
18:56 r
23 23 f
list comprehensions LU 27:40
28 10
pygame.math.Vector2
29 40
39 04
lu normailze vector (vector2) 43 45
52 22
54 35
1 01 16
1 02 14
1 05 09*** level changes
1 15 38
1 22 55
1 30 00
1 32 22
1 34 51
1 36 05
1 41 08

whoohoo!!!!

 last vid!!!!!
 https://www.youtube.com/watch?v=4jdJhUfMycQ&t=0s
28  00
35 50
50 07
done


https://www.youtube.com/watch?v=hEL3wO-EOZg&list=PL8ui5HK3oSiGXM2Pc2DahNu1xXBf7WQh-&index=6



to do- sound
pause when moving to overworld
fix movment glitches? 
last level complete





 lu how to make sprite collisons when the picture collides not just the whole rectangle (convert alpha? )  1 43:13 in thirsd video (overworld video)



*set up file structure 41:40 (gamedata)

Tiled: mapeditor.org
second video
tutorial @ https://www.youtube.com/watch?v=wJMDh9QGRgs *3:09:23
11:14-> create basic level
15:27 
32:02 _saving tiled file
41:04
1:05:45
1:08:40 
1 18 25
1 25 03
1 28 10 
1 45 02
1 56 31 R
2 19 38 f error to be fixed 
2 34 49 su
2 38 56
2 51 31

 
tutorial @ hhttps://www.youtube.com/watch?v=wJMDh9QGRgs *3:09:23
11:40
16:14
24:30
34:07
41:11
57:55
1:05:40
1:09:10
1:11:47 -> 2 hours file path// vs backslash
~1:10 taking image and writing to surface reveiw for ground images
1:16:45
1:24:24
1:34:17
1:38:54/reveiw slightly before to see if better solution
bug to fix-> ~1:45 if up against a wall when jumping, when you land you teleport to the top of the wall (liekly due tyo the sword animation)
1:47:30
1:52:51
1:56:05
1:59:04
2:03:24
2:11:38



1:08:57******

*44 minures level_0 dat


to do 
add in horizon variable for init method sky and clouds (and maybe water?) in level file



follwo up to do's
edit setup level func in level.py
removed from level.py set up level function
        '''for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index*tile_size #left right position
                y = row_index*tile_size #up down position

                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x, y), self.display_surface, self.create_jump_particles) #LU passing a method to a child
                    self.player.add(player_sprite)'''
