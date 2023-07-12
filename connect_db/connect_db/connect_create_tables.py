import pymysql
def connect_mysql():
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='MsQ3Ly%sy', port=3306, db='medical_treatment_db',
                           charset='utf8')
    cur = conn.cursor()
    return cur,conn

def create_tables(cur):
    sql = "CREATE TABLE `department`  (\
  `id` int NOT NULL,\
  `department` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,\
  PRIMARY KEY (`id`) USING BTREE\
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;"
    cur.execute(sql)
    sql = "\
    CREATE TABLE `treatments`  (\
      `id` int NOT NULL AUTO_INCREMENT,\
      `treatment` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,\
      PRIMARY KEY (`id`) USING BTREE\
    ) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;"
    cur.execute(sql)
    sql = "\
CREATE TABLE `disease`  (\
  `id` int NOT NULL AUTO_INCREMENT,\
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,\
  `altername` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,\
  `people` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,\
  `infectivity` tinyint(1) NOT NULL,\
  `under_insurance` tinyint(1) NOT NULL,\
  PRIMARY KEY (`id`) USING BTREE\
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;"
    cur.execute(sql)
    sql = "\
    CREATE TABLE `medicine`  (\
      `id` int NOT NULL AUTO_INCREMENT,\
      `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,\
      `adverse_reaction` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,\
      `instruction` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,\
      PRIMARY KEY (`id`) USING BTREE\
    ) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;"
    cur.execute(sql)
    sql = "\
    CREATE TABLE `symptoms`  (\
      `id` int NOT NULL,\
      `symptom` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,\
      `part` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,\
      PRIMARY KEY (`id`) USING BTREE\
    ) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;"
    cur.execute(sql)
    sql = "\
CREATE TABLE `disease_department`  (\
  `id` int NOT NULL,\
  `disease_id` int NOT NULL,\
  `department_id` int NOT NULL,\
  PRIMARY KEY (`id`) USING BTREE,\
  INDEX `disease_fk`(`disease_id`) USING BTREE,\
  INDEX `department_fk`(`department_id`) USING BTREE\
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;"
    cur.execute(sql)
    sql = "\
CREATE TABLE `disease_medicine`  (\
  `id` int NOT NULL AUTO_INCREMENT,\
  `disease_id` int NOT NULL,\
  `medicine_id` int NOT NULL,\
  PRIMARY KEY (`id`) USING BTREE,\
  INDEX `d_fk`(`disease_id`) USING BTREE,\
  INDEX `medicine_fk`(`medicine_id`) USING BTREE\
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;"
    cur.execute(sql)
    sql = "\
CREATE TABLE `disease_symptom`  (\
  `id` int NOT NULL,\
  `disease_id` int NOT NULL,\
  `symptom_id` int NOT NULL,\
  PRIMARY KEY (`id`) USING BTREE,\
  INDEX `fk2_d`(`disease_id`) USING BTREE,\
  INDEX `fk_symptom`(`symptom_id`) USING BTREE\
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;"
    cur.execute(sql)
    sql = "\
CREATE TABLE `disease_treatment`  (\
  `id` int NOT NULL AUTO_INCREMENT,\
  `disease_id` int NOT NULL,\
  `treament_id` int NOT NULL,\
  PRIMARY KEY (`id`) USING BTREE,\
  INDEX `fk_disease`(`disease_id`) USING BTREE,\
  INDEX `fk_treatment`(`treament_id`) USING BTREE\
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;"
    cur.execute(sql)



    sql = "ALTER TABLE `disease_department` ADD CONSTRAINT `department_fk` FOREIGN KEY (`department_id`) REFERENCES `department` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;"
    cur.execute(sql)
    sql = "ALTER TABLE `disease_department` ADD CONSTRAINT `disease_fk` FOREIGN KEY (`disease_id`) REFERENCES `disease` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;"
    cur.execute(sql)
    sql = "ALTER TABLE `disease_medicine` ADD CONSTRAINT `d_fk` FOREIGN KEY (`disease_id`) REFERENCES `disease` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;"
    cur.execute(sql)
    sql = "ALTER TABLE `disease_medicine` ADD CONSTRAINT `medicine_fk` FOREIGN KEY (`medicine_id`) REFERENCES `medicine` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;"
    cur.execute(sql)
    sql = "ALTER TABLE `disease_symptom` ADD CONSTRAINT `fk2_d` FOREIGN KEY (`disease_id`) REFERENCES `disease` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;"
    cur.execute(sql)
    sql = "ALTER TABLE `disease_symptom` ADD CONSTRAINT `fk_symptom` FOREIGN KEY (`symptom_id`) REFERENCES `symptoms` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;"
    cur.execute(sql)
    sql = "ALTER TABLE `disease_treatment` ADD CONSTRAINT `fk_disease` FOREIGN KEY (`disease_id`) REFERENCES `disease` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;"
    cur.execute(sql)
    sql = "ALTER TABLE `disease_treatment` ADD CONSTRAINT `fk_treatment` FOREIGN KEY (`treament_id`) REFERENCES `treatments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;"
    cur.execute(sql)
    return cur

def insert_initial_data(cur,conn):
    print("start")
    sqls = [
"INSERT INTO `disease`(`id`, `name`, `altername`, `people`, `infectivity`, `under_insurance`) VALUES (1, '鼻炎', '鼻窦炎', '所有人群', 0, 1);",
"INSERT INTO `disease`(`id`, `name`, `altername`, `people`, `infectivity`, `under_insurance`) VALUES (2, '慢性咽炎', '梅核气', '成年人', 0, 1);",
"INSERT INTO `disease`(`id`, `name`, `altername`, `people`, `infectivity`, `under_insurance`) VALUES (3, '中耳炎', NULL, '所有人群', 0, 1);",
"INSERT INTO `disease`(`id`, `name`, `altername`, `people`, `infectivity`, `under_insurance`) VALUES (4, '气管炎', NULL, '中老年人', 0, 1);",
"INSERT INTO `disease`(`id`, `name`, `altername`, `people`, `infectivity`, `under_insurance`) VALUES (5, '感冒', '急性鼻咽炎，急性上呼吸道感染', '所有人群', 1, 0);",
"INSERT INTO `disease`(`id`, `name`, `altername`, `people`, `infectivity`, `under_insurance`) VALUES (6, 'SARS', '非典型肺炎', '所有人群', 1, 0);",
"INSERT INTO `disease`(`id`, `name`, `altername`, `people`, `infectivity`, `under_insurance`) VALUES (7, '小儿哮喘', '小儿支气管哮喘，儿童期哮喘，儿童哮喘', '儿童', 0, 0);",
"INSERT INTO `disease`(`id`, `name`, `altername`, `people`, `infectivity`, `under_insurance`) VALUES (8, '心脏病', NULL, '所有人群', 0, 1);",
"INSERT INTO `disease`(`id`, `name`, `altername`, `people`, `infectivity`, `under_insurance`) VALUES (9, '高血压', '风眩', '中老年人，平时钠盐的摄入量过多的人，父母患有高血压者，摄入动物脂肪较多者', 0, 1);",
"INSERT INTO `disease`(`id`, `name`, `altername`, `people`, `infectivity`, `under_insurance`) VALUES (10, '败血症', '败血病，菌血症', '营养不良，贫血，糖尿病及肝硬化的患者', 0, 1);",
"INSERT INTO `disease`(`id`, `name`, `altername`, `people`, `infectivity`, `under_insurance`) VALUES (11, '中风', '脑卒中，卒中', '中老年人，男性多见', 0, 0);",
"INSERT INTO `disease`(`id`, `name`, `altername`, `people`, `infectivity`, `under_insurance`) VALUES (12, '乙肝', '乙型肝炎', '所有人群，主要见于青少年，绝大多数为10~30岁', 1, 0);",
"INSERT INTO `disease`(`id`, `name`, `altername`, `people`, `infectivity`, `under_insurance`) VALUES (13, '贫血', '血虚', '所有人群，主要是女性，老年人', 0, 1);",
"INSERT INTO `disease`(`id`, `name`, `altername`, `people`, `infectivity`, `under_insurance`) VALUES (14, '低血糖', '饥厥，食厥', '糖尿病患者', 0, 1);",
"INSERT INTO `disease`(`id`, `name`, `altername`, `people`, `infectivity`, `under_insurance`) VALUES (15, '食道癌', '食管癌，膈症，噎膈', '中老年人群', 0, 1);",
"INSERT INTO `disease`(`id`, `name`, `altername`, `people`, `infectivity`, `under_insurance`) VALUES (16, '肺癌', '支气管癌，支气管肺癌', '40岁以上男性，抽烟者', 0, 1);",
"INSERT INTO `disease`(`id`, `name`, `altername`, `people`, `infectivity`, `under_insurance`) VALUES (17, '胃炎', '胃肠感染，肠胃炎', '饮食不节人群，男性多于女性', 0, 1);",
"INSERT INTO `disease`(`id`, `name`, `altername`, `people`, `infectivity`, `under_insurance`) VALUES (18, '幽门螺杆菌感染', '幽门螺旋杆菌感染', '所有人群', 1, 0);",
"INSERT INTO `disease`(`id`, `name`, `altername`, `people`, `infectivity`, `under_insurance`) VALUES (19, '急性胰腺炎', '胰腺炎，胰瘅', '所有人群，发生于妊娠的任何时期,以妊娠晚期及产褥期较多。', 0, 1);",
"INSERT INTO `disease`(`id`, `name`, `altername`, `people`, `infectivity`, `under_insurance`) VALUES (20, '急性肠胃炎', '急性胃肠炎', '所有人群', 0, 1);",
"INSERT INTO `treatments`(`id`, `treatment`) VALUES (1, '药物治疗');",
"INSERT INTO `treatments`(`id`, `treatment`) VALUES (2, '手术治疗');",
"INSERT INTO `treatments`(`id`, `treatment`) VALUES (3, '中医治疗');",
"INSERT INTO `treatments`(`id`, `treatment`) VALUES (4, '食疗');",
"INSERT INTO `treatments`(`id`, `treatment`) VALUES (5, '康复治疗');",
"INSERT INTO `treatments`(`id`, `treatment`) VALUES (6, '支持性治疗');",
"INSERT INTO `treatments`(`id`, `treatment`) VALUES (7, '放化疗');",
"INSERT INTO `treatments`(`id`, `treatment`) VALUES (8, '化学治疗');",
"INSERT INTO `department`(`id`, `department`) VALUES (1, '耳鼻喉科');",
"INSERT INTO `department`(`id`, `department`) VALUES (2, '呼吸内科');",
"INSERT INTO `department`(`id`, `department`) VALUES (3, '传染科');",
"INSERT INTO `department`(`id`, `department`) VALUES (4, '儿科');",
"INSERT INTO `department`(`id`, `department`) VALUES (5, '心血管内科');",
"INSERT INTO `department`(`id`, `department`) VALUES (6, '心胸外科');",
"INSERT INTO `department`(`id`, `department`) VALUES (7, '脑外科');",
"INSERT INTO `department`(`id`, `department`) VALUES (8, '血管外科');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (1, '鼻炎康片', '可见困倦、嗜睡、口渴、虚弱感', '口服，一次4片，一日3次');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (2, '利咽灵片', NULL, '口服，一次3～4片，一日3次');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (3, '头孢氨苄胶囊', '恶心、呕吐、腹泻和腹部不适较为常见', '口服，一次250～500mg，一日4次');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (4, '牛黄解毒丸', NULL, '口服，一次1丸，一日2-3次');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (5, '支气管炎片', NULL, '口服，一次5片，一日3次');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (6, '盐酸氨溴索片', '偶见皮疹、恶心、胃部不适、食欲缺乏、腹痛、腹泻。', '口服。成人，一次1～2片，一日3次，饭后服。');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (7, '感冒清热颗粒', '恶心、呕吐、腹泻、腹痛、腹胀、腹部不适、口干、皮疹、瘙痒、心悸、过敏反应、呼吸困难等。', '开水冲服。一次1袋，一日2次。');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (8, '小儿热速清糖浆', NULL, '口服，一岁以内，一次2.5～5毫升，一岁至三岁，一次5～10毫升，三岁至七岁，一次10～15毫升，七岁至十二岁，一次15～20毫升，一日3～4次。');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (9, '盐酸乙胺丁醇片', '视力模糊、眼痛、 红绿色盲或视力减退、视野缩小，视力变化可为单侧或双侧', '结核初治，按体重15mg/kg，每日一次顿 服，或每次口服25-30mg/kg，最高10片，每周3次；或50mg/kg，最高10片，每周2 次。结核复治，按体重25mg/kg,每日一 次顿服，连续60天，继以按体重15mgAg，每日一次顿服。');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (10, '孟鲁司特纳咀嚼片', '腹痛和头痛', '每日1次睡前服用');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (11, '盐酸多巴酚丁胺', '可有心悸、恶心、头痛、胸痛、气短等', '将多巴酚丁胺加于5%葡萄糖液或0.9%氯化钠注射液中稀释后，以滴速每分钟2.5-10μg/㎏给予，在每分钟15μg/㎏以下的剂量时，心率和外周血管阻力基本无变化；偶用每分钟﹥15μg/㎏，但需注意过大剂量仍然有可能加速心率并产生心律失常。');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (12, '奥美沙坦酯片', '头晕', '起始剂量为20mg，每日1次。对经2周治疗后仍需进一步降低血压的患者，剂量可增至40mg。');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (13, '盐酸阿罗洛尔片', '心动过缓141例、眩晕及站立不稳、乏力及倦怠感', '每日10mg');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (14, '氟氯西林钠胶囊', '过敏现象；偶有斑疹、腹泻、恶心、消化不良。', '成人：每次1粒，每日四次；应于饭前至少半小时服用，重症感染，剂量可加倍。');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (15, '脑络通胶囊', NULL, '口服，一次1～2粒，一日3次。');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (16, '恩替卡韦分散片', '头痛、疲劳、眩晕、恶心', '口服，每天一次，每次0.5mg。');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (17, '维生素B12片', '有低血钾及高尿酸血症等不良反应报道。', '口服，一日1-4片或隔日2-8片。');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (18, '当归补血口服液', NULL, '口服。一次10毫升，一日2次。');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (19, '复方天仙胶囊', NULL, '口服，一次2-3粒，一日3次。');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (20, '益肺清化颗粒', '偶见恶心，腹泻。', '口服。一次2袋，一日3次。');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (21, '康复新液', NULL, '口服，一次10ml，一日3次；外用，用医用纱 布浸透药液后敷患处，感染创面先清创后再用本品冲洗，并用浸透本品的纱布填塞或敷用。');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (22, '复方雷尼替丁片', '常见恶心、便秘、皮疹、乏力、头痛、头晕。', '口服，成人一次1片，一日2次。');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (23, '克拉霉素胶囊', '口腔异味，腹痛、腹泻、恶心、呕吐等胃肠道反应，头痛', '口服，常用量一次0.25g（2粒），每12小时1次。');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (24, '醋酸奥曲肽注射', '注射局部反应，包括疼痛，注射部位针剌或烧灼感，伴红肿；胃肠道反应，包括食欲不振、恶心、呕吐、痉挛性腹痛、胀气、稀便、腹泻及脂肪痢。', '持续静脉滴注0.025毫克/小时。最多治疗5天，可用生理盐水稀释或葡萄糖液稀释。');",
"INSERT INTO `medicine`(`id`, `name`, `adverse_reaction`, `instruction`) VALUES (25, '枫蓼肠胃康合剂', NULL, '口服，一次10ml，一日3次。浅表性胃炎15天为一疗程。');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (1, '咽部充血', '咽喉');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (2, '咽痛', '咽喉');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (3, '吞咽障碍', '咽喉');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (4, '听力减退', '耳');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (5, '耳痛', '耳');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (6, '传导性耳鸣', '耳');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (7, '流鼻涕', '鼻');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (8, '鼻塞', '鼻');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (9, '嗅觉丧失', '鼻');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (10, '头痛', '头部');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (11, '咳嗽', '气管');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (12, '咳痰', '气管');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (13, '发热', '全身');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (14, '呼吸困难', '肺');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (15, '支气管平滑肌痉挛', '肺');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (16, '低氧血症', '血液血管');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (17, '心动过速', '心脏');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (18, '心悸', '心脏');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (19, '窒息', '肺');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (20, '血压高', '血液血管');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (21, '打喷嚏', '鼻');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (22, '败血症', '全身');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (23, '感觉障碍', '头部');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (24, '偏瘫', '全身');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (25, '肝肿大', '肝');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (26, '乙肝表面抗原阳性', '肝');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (27, '肝功能异常', '肝');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (28, '乏力', '全身');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (29, '食欲减退', '全身');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (30, '空腹低血糖', '血液血管');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (31, '进食困难', '食管');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (32, '肺部肿块', '肺');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (33, '腹痛', '胃');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (34, '恶心呕吐', '胰腺');",
"INSERT INTO `symptoms`(`id`, `symptom`, `part`) VALUES (35, '急腹症', '胰腺');",
"INSERT INTO `disease_department`(`id`, `disease_id`, `department_id`) VALUES (1, 1, 1);",
"INSERT INTO `disease_department`(`id`, `disease_id`, `department_id`) VALUES (2, 2, 1);",
"INSERT INTO `disease_department`(`id`, `disease_id`, `department_id`) VALUES (3, 3, 1);",
"INSERT INTO `disease_department`(`id`, `disease_id`, `department_id`) VALUES (4, 4, 2);",
"INSERT INTO `disease_department`(`id`, `disease_id`, `department_id`) VALUES (5, 5, 3);",
"INSERT INTO `disease_department`(`id`, `disease_id`, `department_id`) VALUES (6, 5, 2);",
"INSERT INTO `disease_department`(`id`, `disease_id`, `department_id`) VALUES (7, 6, 3);",
"INSERT INTO `disease_department`(`id`, `disease_id`, `department_id`) VALUES (8, 6, 2);",
"INSERT INTO `disease_department`(`id`, `disease_id`, `department_id`) VALUES (9, 7, 4);",
"INSERT INTO `disease_department`(`id`, `disease_id`, `department_id`) VALUES (10, 7, 2);",
"INSERT INTO `disease_department`(`id`, `disease_id`, `department_id`) VALUES (11, 8, 5);",
"INSERT INTO `disease_department`(`id`, `disease_id`, `department_id`) VALUES (12, 8, 6);",
"INSERT INTO `disease_department`(`id`, `disease_id`, `department_id`) VALUES (13, 9, 5);",
"INSERT INTO `disease_department`(`id`, `disease_id`, `department_id`) VALUES (14, 9, 6);",
"INSERT INTO `disease_department`(`id`, `disease_id`, `department_id`) VALUES (15, 10, 2);",
"INSERT INTO `disease_department`(`id`, `disease_id`, `department_id`) VALUES (16, 10, 5);",
"INSERT INTO `disease_department`(`id`, `disease_id`, `department_id`) VALUES (17, 11, 7);",
"INSERT INTO `disease_department`(`id`, `disease_id`, `department_id`) VALUES (18, 11, 8);",
"INSERT INTO `disease_department`(`id`, `disease_id`, `department_id`) VALUES (19, 12, 3);",
"INSERT INTO `disease_department`(`id`, `disease_id`, `department_id`) VALUES (24, 16, 2);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (1, 1, 1);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (2, 2, 2);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (3, 3, 3);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (4, 3, 4);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (5, 4, 5);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (6, 5, 6);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (7, 5, 7);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (8, 6, 8);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (9, 6, 9);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (10, 7, 10);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (11, 8, 11);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (12, 9, 12);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (13, 9, 13);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (14, 10, 14);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (15, 11, 15);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (16, 12, 16);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (17, 13, 17);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (18, 14, 18);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (19, 15, 19);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (20, 16, 20);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (21, 17, 21);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (22, 17, 22);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (23, 18, 23);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (24, 19, 24);",
"INSERT INTO `disease_medicine`(`id`, `disease_id`, `medicine_id`) VALUES (25, 20, 25);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (1, 3, 4);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (2, 3, 5);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (3, 3, 6);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (4, 2, 1);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (5, 2, 2);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (6, 2, 3);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (7, 1, 7);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (8, 1, 8);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (9, 1, 9);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (10, 1, 10);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (11, 4, 11);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (12, 4, 12);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (13, 6, 13);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (14, 6, 11);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (15, 6, 14);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (16, 7, 15);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (17, 7, 14);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (18, 7, 16);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (19, 8, 17);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (20, 8, 18);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (21, 8, 19);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (22, 9, 20);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (23, 9, 10);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (24, 9, 18);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (25, 5, 21);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (26, 5, 13);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (27, 5, 11);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (28, 10, 10);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (29, 10, 13);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (30, 10, 18);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (31, 11, 23);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (32, 11, 10);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (33, 11, 24);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (34, 12, 27);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (35, 12, 25);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (36, 12, 26);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (37, 13, 28);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (38, 13, 29);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (39, 14, 17);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (40, 14, 30);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (41, 15, 3);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (42, 15, 31);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (43, 16, 11);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (44, 16, 12);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (45, 16, 32);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (46, 17, 29);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (47, 17, 33);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (48, 18, 33);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (49, 18, 34);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (50, 19, 33);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (51, 19, 34);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (52, 19, 35);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (53, 20, 13);",
"INSERT INTO `disease_symptom`(`id`, `disease_id`, `symptom_id`) VALUES (54, 20, 34);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (1, 1, 1);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (2, 2, 1);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (3, 3, 1);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (4, 3, 2);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (5, 4, 1);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (6, 4, 3);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (7, 4, 4);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (8, 5, 1);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (9, 7, 1);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (10, 8, 1);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (11, 9, 1);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (12, 9, 4);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (13, 10, 1);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (14, 11, 5);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (15, 11, 6);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (16, 12, 1);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (17, 12, 4);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (18, 13, 1);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (19, 13, 4);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (20, 14, 1);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (21, 14, 6);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (22, 15, 2);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (23, 15, 7);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (24, 16, 2);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (25, 16, 8);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (26, 17, 1);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (27, 18, 1);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (28, 19, 1);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (29, 19, 2);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (30, 20, 1);",
"INSERT INTO `disease_treatment`(`id`, `disease_id`, `treament_id`) VALUES (31, 20, 6);"]
    for sql in sqls :
        cur.execute(sql)
        conn.commit()
def initinal_database():
    result = connect_mysql()
    cur = result[0]
    conn = result[1]
    cur = create_tables(cur=cur)
    insert_initial_data(cur=cur,conn=conn)
    return

if __name__ == '__main__':
    initinal_database()
