class birb {
    constructor() {
      this.position = createVector(random(width), random(width));
      this.velocity = p5.Vector.random2D();
      this.acceleration = createVector(0, 0);
      this.maxForce=0.2;
      this.maxSpeed=3;
    }
    update(){
        this.position.add(this.velocity);
        this.position.x=(this.position.x%width+width)%width;
        this.position.y=(this.position.y%height+height)%height;

        this.velocity.add(this.acceleration).limit(this.maxSpeed);
    }
    show(){
        console.log(this.position.x)
        ellipse(this.position.x, this.position.y, 8)
    }
    align(boids) {
        let perceptionRadius = 20;
        let steering = createVector();
        let total = 0;
        for (let other of boids) {
          let d = dist(this.position.x, this.position.y, other.position.x, other.position.y);
          if (other != this && d < perceptionRadius) {
            steering.add(other.velocity);
            total++;
          }
        }
        if (total > 0) {
          steering.div(total);
          steering.setMag(this.maxSpeed);
          steering.sub(this.velocity);
          steering.limit(this.maxForce);
        }
        return steering;
      }
    
      separation(boids) {
        let perceptionRadius = 15;
        let steering = createVector();
        let total = 0;
        for (let other of boids) {
          let d = dist(this.position.x, this.position.y, other.position.x, other.position.y);
          if (other != this && d < perceptionRadius) {
            let diff = p5.Vector.sub(this.position, other.position);
            diff.div(d * d);
            steering.add(diff);
            total++;
          }
        }
        if (total > 0) {
          steering.div(total);
          steering.setMag(this.maxSpeed);
          steering.sub(this.velocity);
          steering.limit(this.maxForce);
        }
        return steering;
      }
    
      cohesion(boids) {
        let perceptionRadius = 25;
        let steering = createVector();
        let total = 0;
        for (let other of boids) {
          let d = dist(this.position.x, this.position.y, other.position.x, other.position.y);
          if (other != this && d < perceptionRadius) {
            steering.add(other.position);
            total++;
          }
        }
        if (total > 0) {
          steering.div(total);
          steering.sub(this.position);
          steering.setMag(this.maxSpeed);
          steering.sub(this.velocity);
          steering.limit(this.maxForce);
        }
        return steering;
      }
    
      flock(boids) {
        let alignment = this.align(boids);
        let cohesion = this.cohesion(boids);
        let separation = this.separation(boids);
    
        alignment.mult(alignStrength);
        cohesion.mult(cohesionStrength);
        separation.mult(separationStrength);
    
        this.acceleration.add(alignment);
        this.acceleration.add(cohesion);
        this.acceleration.add(separation);
      }    
}

const flock=[];
const num_birbs=100;
const alignStrength=3;
const cohesionStrength=0.7;
const separationStrength=8;

function setup() {
  createCanvas(windowWidth, windowHeight);
  for (let i = 0; i < num_birbs; i++) {
    flock.push(new birb());
  }
}


function draw() {
  background('white');
  fill('lightpink');
  noStroke();
  ellipse(0, 0, 30)
  ellipse(width, height, 30)
  for (let bird of flock){
    bird.flock(flock)
    bird.update()
    bird.show()
  };
}

function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
}