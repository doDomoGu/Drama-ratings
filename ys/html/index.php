<!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta charset="utf-8"/>
</head>
<body>
<?php
    $conf = parse_ini_file('../conf.ini',true);


    $dbh = new PDO('mysql:host='.$conf['MYSQL']['host'].';dbname='.$conf['MYSQL']['db'], $conf['MYSQL']['user'], $conf['MYSQL']['password']);
    $season = [
        1=>'冬季',
        2=>'春季',
        3=>'夏季',
        4=>'秋季'
    ]
?>
<?php if(isset($_GET['act']) && $_GET['act']=='drama'):?>
    <div>
        <a href="index.php" >Back ></a>
    </div>
    <?php
    $page = $dbh->query('SELECT * from `page` where id = '.$_GET['p_id'])->fetch();

    $dramas = $dbh->query('SELECT d.id,d.title,ts.name as `tv`, pt.name as `time`, d.rating_avg, d.trend from `drama` d join tv_station ts on d.tv_id = ts.id join play_time pt on d.time_id = pt.id where page_id = '.$_GET['p_id']);

    $epi_num = $dbh->query('SELECT max(e.num) from `episode` e join `drama` d on e.drama_id = d.id where e.enable = 1 and d.page_id = '.$_GET['p_id'])->fetchColumn();
    
    ?>
    <div><?=$page['year'].' / '.$season[$page['season']]?></div>
    <ul style="list-style:none;padding-left:0;font-weight:bold;">
        <li>
            <span style="display:inline-block;width:30px;">#</span>
            <span style="display:inline-block;width:400px;">剧名</span>
            <span style="display:inline-block;width:60px;">电视台</span>
            <span style="display:inline-block;width:60px;">时段</span>

            <?php for($i=1;$i<=$epi_num;$i++):?>
            <span style="display:inline-block;width:60px;"><?=$i?></span>    
            <?php endfor;?>
            <span style="display:inline-block;width:60px;">平均</span>
            <span style="display:inline-block;width:100px;">走势</span>
        </li>
    </ul>
    <ul style="list-style:none;padding-left:0;">
        <?php foreach($dramas as $d):?>
            <?php 
                $episodes = $dbh->query('SELECT `num`,`rating` from `episode` where drama_id = '.$d['id'].' and `enable` = 1')->fetchAll();
            ?>
            <li style="height:36px;">
                <span style="display:inline-block;width:30px;"><?=$d['id']?></span>
                <span style="display:inline-block;width:400px;"><?=$d['title']?></span>
                <span style="display:inline-block;width:60px;"><?=$d['tv']?></span>
                <span style="display:inline-block;width:60px;"><?=$d['time']?></span>
                <?php for($i=0;$i<$epi_num;$i++):?>
                    <span style="display:inline-block;width:60px;"><?=isset($episodes[$i])?$episodes[$i]['rating']:''?></span>    
                <?php endfor;?>
                <span style="display:inline-block;width:60px;"><?=$d['rating_avg']?></span>
                <span style="display:inline-block;width:100px;"><?=$d['trend']?></span>
            </li>
        <?php endforeach;?>
    </ul>
<?php else:?>

    <?php
    $pages = $dbh->query('SELECT * from `page` order by year asc ,season asc');


    ?>
    <ul>
    <?php foreach($pages as $p):?>
        <?php
            $sql = 'SELECT * from drama where page_id = '.$p['id'];
            $res = $dbh->prepare($sql);
            $res->execute();
            $num = $res->rowCount();

        ?>
        <li>
            <span style="display:inline-block;width:200px;"><?=$p['year']?></span>
            <span style="display:inline-block;width:200px;"><?=$season[$p['season']]?></span>
            <span style="display:inline-block;width:200px;"><?=$p['url']?></span>
            <span style="display:inline-block;width:200px;"><a href="?act=drama&p_id=<?=$p['id']?>"><?=$num?></a></span>
        </li>
    <?php endforeach;?>
    </ul>
<?php endif;?>
</body>
</html>

