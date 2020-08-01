import React, {useState, useEffect} from 'react';
import {
  Row,
  Col,
  Container,
} from 'reactstrap';

import Painting from '../components/Painting';
import {getPaintings} from '../api/painting';

function getTagsFromSearch(url) {
  const query = url.substr(1);
  return query.substr(query.indexOf('=') + 1).split(',');
}

function Home(props) {

  const [tags, setTags] = useState([]);
  const [paintings, setPaintings] = useState([{
    id: '0',
    name: '',
    price: 0,
    width: 0,
    height: 0,
    tags: [],
    thumbnail: '',
    description: '',
  }]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setTags(getTagsFromSearch(props.location.search));
    setLoading(true);
    getPaintings().then(data => {
      if (data.length !== 0)
        setPaintings(data);
    }).catch(err => {
      console.log(err);
    }).finally(() => {
      setLoading(false);
    });
  }, [setTags, props, setPaintings, setLoading]);

  return (
    <Container>
      <br/>

      <Row className={loading ? 'd-none' : ''}>
        {
          paintings.map((painting, index) => (
            <Col className="mb-4" md={4} sm={12} xs={12} key={painting.id}>
              <Painting painting={painting}/>
            </Col>
          ))
        }
      </Row>
    </Container>
  );
}

export default Home;
