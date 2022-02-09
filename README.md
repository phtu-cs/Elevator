# Elevator
 
## Usage 

```
python elevator.py
```
It will output 


> INPUT COMMAND EXAMPLE: "to 10" means pushing the button inside the elevator to the 10th floor; 
"up 5" means pushing the up button on the 5th floor outside the elevator; 
"down 4" means pushing the down button on the 4th floor outside the elevator; 
"where" outputs the positon of the elevator


Then you can start to interact with the elevator, for example, by writing below in the command prompt

```
where
```

It will output

> elevator is currently on 1 floor.

Then you can write

```
to 5
```

The elevator will go upstairs to 5th floor. The program will output

> someone inside the elevator want to go to 5 floor.
> 
> Elevator is going up, currently on 2 floor.
> 
> Elevator is going up, currently on 3 floor.
> 
> Elevator is going up, currently on 4 floor.
> 
> Elevator is going up, currently on 5 floor.
> 
> Door opens, at 5 floor.
> 
> Please enter destination in 5s: 
> 
> Door closes, at 5 floor
> 
> Elevator stops, currently on 5 floor

Then if you write

```
down 10
```
The output will be 

> someone on 10 floor wants to go downstairs.
> 
> Elevator is going up, currently on 6 floor.
> 
> Elevator is going up, currently on 7 floor.
> 
> Elevator is going up, currently on 8 floor.
> 
> Elevator is going up, currently on 9 floor.
> 
> Elevator is going up, currently on 10 floor.
> 
> Door opens, at 10 floor.
> 
> Please enter destination in 5s: 
> 
> Door closes, at 10 floor
> 
> Elevator stops, currently on 10 floor

You can interact with the elevator regardless of the status of the elevator. In other words, you can input any commands anytime, as long as it is in correct format.
If you write

```
a b
```
The output will be

> Wrong format! Please input again! (e.g. "down 9", "up 5", "to 4") Note there is no "down 1" and "up 10"
