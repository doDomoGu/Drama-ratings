<!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta charset="utf-8"/>
</head>
<body>
<?php
    $dbh = new PDO('mysql:host=localhost;dbname=ys', 'gljgljglj', 'gljgogo');
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

    $dramas = $dbh->query('SELECT d.title,ts.name as tv,pt.name as time from `drama` d join tv_station ts on d.tv_id = ts.id join play_time pt on d.time_id = pt.id where page_id = '.$_GET['p_id']);
    ?>
    <div><?=$page['year'].' / '.$season[$page['season']]?></div>
    <ul>
        <?php foreach($dramas as $d):?>
            <li>
                <span style="display:inline-block;width:200px;"><?=$d['title']?></span>
                <span style="display:inline-block;width:200px;"><?=$d['tv']?></span>
                <span style="display:inline-block;width:200px;"><?=$d['time']?></span>
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

