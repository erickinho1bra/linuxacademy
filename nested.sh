#/bin/bash
# demo of nested function and some abstraction

# global virable
GENDER=$1

##### Function definitions - start

# create a human being
funcHuman () {
  ARMS=2
  LEGS=2

  funcMale () {
    BEARD=1

    echo "This man has $ARMS arms AND $LEGS legs, with $BEARD beard(s)..."
    echo ""
  }

  funcFemale () {
    echo "This woman has $ARMS arms and $LEGS legs, with $BEARD beards(s)..."
    echo ""
  }

}

##### Function definitions - stop


##### Script - start

clear
echo "Determining characteristics of the gender $GENDER"

if [ "$GENDER" == "male" ] ; then
  funcHuman
  funcMale
else
  funcHuman
  funcFemale
fi

##### Script - stop
