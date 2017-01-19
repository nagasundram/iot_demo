# Database Schema
Rooms Table

rooms
+-------+---------+------+-----+---------+----------------+
| Field | Type    | Null | Key | Default | Extra          |
+-------+---------+------+-----+---------+----------------+
| id    | int(11) | NO   | PRI | NULL    | auto_increment |
| name  | text    | YES  |     | NULL    |                |
+-------+---------+------+-----+---------+----------------+

room_details
+----------+------------+------+-----+---------+----------------+
| Field    | Type       | Null | Key | Default | Extra          |
+----------+------------+------+-----+---------+----------------+
| id       | int(11)    | NO   | PRI | NULL    | auto_increment |
| room_id  | int(11)    | YES  | MUL | NULL    |                |
| in_time  | datetime   | YES  |     | NULL    |                |
| out_time | datetime   | YES  |     | NULL    |                |
| status   | tinyint(1) | YES  |     | NULL    |                |
+----------+------------+------+-----+---------+----------------+
