# EMG Controlled Wheelchair
## EMG Acquisioin Circuit
Each module can be implemented on LTspice <br>
Steps to be followed for EMG acquisition
1. Amplification
2. Filtering
3. Rectification
4. Integration
5. Inversion
<br>

## Control using Raspberry Pi Pico
The provided code can be uploaded on Raspberry Pi Pico <br>
### Thresholds
* 0.1-0.75V Forward
* 0.85-1.6V Left
* 1.7-2.45V Right
* 2.55-3.3V Reverse

### Pin connections
* EMG: 27
* Speed Control: 26
* Motor Driver
  * enA: 4
  * enB: 5
  * IN1: 6
  * IN2: 7
  * IN3: 8
  * IN4: 9
