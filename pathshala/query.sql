select p.sno,count(c.sentiment) from playlist p, videos v ,comments c where p.sno=v.sno and v.ID=c.id group by p.sno;

select p.sno,count(c.sentiment) from playlist p, videos v ,comments c where p.sno=v.sno and v.ID=c.id group by p.sno having c.sentiment='True';

 select p.sno,c.sentiment,count(c.sentiment) as count from playlist p, videos v ,comments c where p.sno=v.sno and v.ID=c.id group by p.sno,c.sentiment having c.sentiment='True' order by p.sno;

(session.query(playlist p, videos v ,comments c)
        .join(p.sno)
        .join(c.sentiment)
        .join(count(c.sentiment))
        .filter(p.sno==v.sno and v.ID==c.id and c.sentiment='True')
        .group_by(p.sno)
        .order_by(p.sno)
        ).all()