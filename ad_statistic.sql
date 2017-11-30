
DROP TABLE IF EXISTS `ad_statistic`;
CREATE TABLE `ad_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `apk_channel_id` int(11) NOT NULL,
  `game_id` int(11) NOT NULL,
  `type` int(11) NOT NULL,
  `server` int(1) NOT NULL,
  `source` varchar(50) DEFAULT NULL,
  `subsource` varchar(50) DEFAULT NULL,
  `visit` int(10) NOT NULL DEFAULT '0',
  `finish` int(10) NOT NULL DEFAULT '0',
  `click` int(10) NOT NULL DEFAULT '0',
  `ipload` int(10) NOT NULL DEFAULT '0',
  `ipfinish` int(10) NOT NULL DEFAULT '0',
  `ipclick` int(10) NOT NULL DEFAULT '0',
  `collect_datetime` datetime NOT NULL,
  `load_time` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `uniq_apk_channel_game_type_time_server` (`apk_channel_id`,`game_id`,`type`,`collect_datetime`,`server`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `time_control`;
CREATE TABLE `time_control` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `server` varchar(10) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

