# Einleitung

## Motivation

SpinalHDL wurde entwickelt, um die Produktivitäts- und Wartbarkeitsprobleme klassischer Hardwarebeschreibungssprachen (HDLs) wie VHDL und Verilog zu beheben. Es ermöglicht Entwicklern, wiederverwendbare und skalierbare digitale Designs in einer modernen, typgesicherten Umgebung zu erstellen – durch die Integration in die Programmiersprache Scala.

## Überblick über traditionelle HDLs (VHDL/Verilog)

Traditionelle HDLs wie VHDL und Verilog wurden in den 1980er Jahren entwickelt. Obwohl sie bis heute Standard sind, haben sie erhebliche Nachteile:

- **Geringe Abstraktion:** Strukturelle Wiederverwendung und Parametrisierung sind schwierig.  
- **Schlechte Fehlerdiagnose:** Kompilierungsfehler liefern oft kryptische Fehlermeldungen.  
- **Statischer Code:** Keine Möglichkeit zur dynamischen Erzeugung von Komponenten.  
- **Mangelnde Integration moderner Softwarepraktiken:** Keine Unit-Tests, keine IDE-Integration auf hohem Niveau.

## Warum die Abkehr sinnvoll ist

Moderne Hardwareentwicklungsprojekte profitieren von den Prinzipien der Softwareentwicklung:

- Wiederverwendbarkeit durch Module  
- Testbarkeit durch Simulation und automatisierte Tests  
- Abstraktion durch objektorientierte und funktionale Programmierung  

SpinalHDL vereint diese Stärken mit der Möglichkeit, dennoch synthetisierbaren VHDL- oder Verilog-Code zu generieren.

---

#  Grundlagen von SpinalHDL

SpinalHDL ist eine Hardwarebeschreibungssprache, die als **Domain Specific Language (DSL)** in **Scala** implementiert ist. Sie bietet gegenüber VHDL und Verilog eine moderne, typensichere und modulare Beschreibung von Schaltungen.

## Variablendeklaration in SpinalHDL

Die wichtigsten Typen zur Signalbeschreibung:

| Typ    | Beschreibung                   | Beispiel                     |
|--------|--------------------------------|------------------------------|
| `Bool` | Ein einzelnes Bit (true/false) | `val myBit = Bool()`         |
| `UInt` | Unsigned Integer (z. B. 8 Bit) | `val count = UInt(8 bits)`   |
| `SInt` | Signed Integer                 | `val x = SInt(16 bits)`      |
| `Bits` | Bit-Vektor ohne Interpretation | `val raw = Bits(4 bits)`     |

> In SpinalHDL beschreibt `val` eine **konstante Referenz auf ein Signalobjekt** – nicht das Signal selbst wie in Verilog.
## Signale vs. Register

```scala
val a = UInt(8 bits)       // Kombinatorisch (wire)
val b = Reg(UInt(8 bits))  // Getaktetes Register
```

- `Reg(...)` erzeugt ein Flip-Flop (Register) mit Initialwert:  

```scala
val count = Reg(UInt(4 bits)) init(0)
```

## Steuerstrukturen

Wie in Scala aber spezialisiert für Hardwarelogik:

```scala
when(cond) {
  // true-Zweig
} elsewhen(otherCond) {
  // anderer Zweig
} otherwise {
  // fallback-Zweig
}
```

Beispiel:

```scala
val out = Bool()
when(io.a === io.b) {
  out := True
} otherwise {
  out := False
}
```

## Bundles (Schnittstellen)

Ein `Bundle` ist wie ein `struct`:

```scala
val io = new Bundle {
  val start = in Bool()
  val done  = out Bool()
  val value = in UInt(8 bits)
}
```
 Alle Signale im Bundle sind typisiert (`in`, `out`, `inout`).

## Vektoren und Arrays

```scala
val vec = Vec(UInt(8 bits), 4)
val arr = Array.fill(4)(UInt(8 bits))
```
Vektoren erlauben z. B. Busse, Speicher, Registergruppen.

## Komponentenstruktur

Eine Hardwareeinheit (Modul) ist eine Klasse, die von `Component` erbt:

```scala
class MyModule extends Component {
  val io = new Bundle {
    val a = in UInt(8 bits)
    val b = in UInt(8 bits)
    val result = out UInt(8 bits)
  }

  io.result := io.a + io.b
}
```

## Top-Level mit Verilog-Ausgabe

```scala
object MyModuleVerilog {
  def main(args: Array[String]): Unit = {
    SpinalVerilog(new MyModule)
  }
}
```

## Typisches Verhalten vs. VHDL

| Aktion                | VHDL                  | SpinalHDL                         |
|-----------------------|-----------------------|-----------------------------------|
| Signal zuweisen       | `a <= b;`             | `a := b`                          |
| Wenn-Bedingung        | `if...elsif...else`   | `when...elsewhen...otherwise`    |
| Register mit Reset    | Prozess mit Reset     | `Reg(...) init(...)`              |
| Strukturierte I/Os    | Record / Port Map     | `Bundle`, `in/out`                |

## Besonderheiten

- **stark typisiert** – viele Fehler werden vom Compiler erkannt  
- **parametrisierbar** – Bausteine können generisch sein  
- **simulationsfähig** – direkt in Scala testbar  
- **Verilog/VHDL-Ausgabe** – leicht integrierbar  

## TL;DR für Anfänger

| Du willst …         | … dann nutze             |
|---------------------|--------------------------|
| 1 Bit Signal        | `Bool()`                 |
| 8 Bit Zähler        | `Reg(UInt(8 bits))`      |
| Multiplexer         | `Mux(sel, a, b)`         |
| Verzweigung         | `when { ... }`           |
| Interface           | `new Bundle { ... }`     |

---

#  Struktur und Aufbau eines SpinalHDL-Projekts

## Ordnerstruktur

```text
my-spinal-project/
├── build.sbt
├── src/
│   ├── main/
│   │   └── scala/           // SpinalHDL-Komponenten
│   └── test/
│       └── scala/           // Simulation und Unit-Tests
├── generated/               // generierter Verilog/VHDL
└── README.md
```

## Entwicklungsumgebung

- **IDE:** IntelliJ IDEA mit Scala-Plugin  
- **Build-Tool:** sbt (Scala Build Tool)  
- **Simulation:** Verilator oder GHDL  

## Beispiel-Kommando

```bash
sbt compile
sbt run
```

---

#  Vorteile von SpinalHDL gegenüber traditionellen HDLs

## Syntax und Typsicherheit

SpinalHDL basiert auf Scala und profitiert von einer modernen, stark typisierten Syntax. Typfehler oder Verbindungsprobleme werden bereits zur Kompilierzeit erkannt, was typische Laufzeitfehler klassischer HDLs verhindert.

## Abstraktion und Wiederverwendbarkeit

Mit Vererbung, generischen Klassen und parametrisierten Modulen können Komponenten einfach angepasst und wiederverwendet werden. Schleifen, Funktionen, Bedingungen und sogar Fabriken für Komponenten sind möglich.

## Fehlerdiagnose

Fehlermeldungen in SpinalHDL enthalten vollständige Stacktraces aus Scala und zeigen direkt auf die Quelle des Problems  z. B. eine ungültige Zuweisung oder ein Signal, das mehrfach getrieben wird.

## Simulation & Debugging

Durch die Integration mit Scala kann SpinalHDL direkt in der JVM simuliert werden. Mit `SimConfig` und `ScalaTest` lassen sich präzise, wiederholbare Testcases erstellen.

---

#  Entwicklungsworkflow

In SpinalHDL folgt ein typischer Designprozess drei Phasen:

1. **Komponentenbeschreibung** (Design)
2. **Simulation & Verifikation** (Test)
3. **Codegenerierung** (Export in Verilog/VHDL)

##   Komponentenbeschreibung

Hier wird das gewünschte Verhalten in einem Modul (Component) beschrieben.

```scala
class Adder extends Component {
  val io = new Bundle {
    val a, b = in UInt(8 bits)
    val result = out UInt(8 bits)
  }
  io.result := io.a + io.b
}
```
###  Erklärung :

- `class Adder extends Component`: definiert eine neue SpinalHDL-Komponente.
- `val io = new Bundle { ... }`: legt die I/O-Schnittstelle fest.
  - `a`, `b`: 8-Bit Eingänge (z. B. zwei Summanden)
  - `result`: 8-Bit Ausgang (Summe)
- `io.result := io.a + io.b`: beschreibt die Logik: Addition von `a` und `b`, das Ergebnis wird ausgegeben.

**Das ist reine Kombinatorik**, kein Register (d.h. keine Speicherung, kein Takt).

##   Simulationsmöglichkeiten

Mit SpinalHDL kannst du direkt in Scala simulieren.

```scala
SimConfig.withWave.compile(new Adder).doSim { dut =>
  dut.io.a #= 4
  dut.io.b #= 7
  dut.clockDomain.forkStimulus(10)
  dut.clockDomain.waitSampling()
  assert(dut.io.result.toInt == 11)
}
```
###  Erklärung :

- `SimConfig.withWave`: Aktiviert Wellenform-Ausgabe (`.vcd`).
- `compile(new Adder)`: kompiliert die Adder-Komponente für Simulation.
- `doSim { dut => ... }`: definiert, was im Simulationslauf passieren soll.

**Innerhalb des Blocks:**
- `dut.io.a #= 4`: Setzt Eingang `a` auf 4
- `dut.io.b #= 7`: Setzt Eingang `b` auf 7
- `forkStimulus(10)`: Erzeugt Taktsignal mit Periodendauer 10
- `waitSampling()`: Wartet auf eine steigende Taktflanke
- `assert(...)`: Prüft, ob das Ergebnis tatsächlich 11 ist

>  Hinweis: Die Simulation verwendet dieselbe Logik wie der Synthese-Code, sie ist somit **cycle-accurate**.

## Code generieren (Verilog/VHDL)

Mit einem einfachen Aufruf generierst du RTL-Code:

```scala
SpinalVerilog(new Adder)
SpinalVhdl(new Adder)
```
- `SpinalVerilog(...)`: erzeugt eine `.v`-Datei (Verilog)
- `SpinalVhdl(...)`: erzeugt eine `.vhd`-Datei (VHDL)
- Die Datei enthält exakt das, was von Tools wie **Vivado**, **Quartus**, **Yosys**, etc. verarbeitet werden kann

 Der generierte Code wird im aktuellen Arbeitsverzeichnis gespeichert oft in einem Unterordner wie `./rtl/` oder `./simWorkspace/Adder`.


##  Zusammengefasst:

| Schritt          | Ziel                           | Beispiel                          |
|------------------|--------------------------------|-----------------------------------|
| Komponentenbau   | Schaltung entwerfen            | `new Adder`                       |
| Simulation       | Verhalten testen               | `doSim { ... }`                   |
| Codegenerierung  | Verilog/VHDL für Synthesis     | `SpinalVerilog(...)

---

#  Praxisbeispiele

## Comparator

Ein Comparator vergleicht zwei Werte (`a` und `b`) und erzeugt Ausgänge für:
- Gleichheit (`equal`)
- Größer-als (`greater`)
- Kleiner-als (`less`)

**Aufbau des Moduls**

```scala
class Comparator(width: Int) extends Component {
  val io = new Bundle {
    val a      = in UInt(width bits)
    val b      = in UInt(width bits)
    val equal  = out Bool()
    val greater = out Bool()
    val less   = out Bool()
  }

  io.equal   := io.a === io.b
  io.greater := io.a > io.b
  io.less    := io.a < io.b
}
```
**Was macht das Modul?**

- Es nimmt zwei `UInt`-Eingänge `a` und `b`.
- Es vergleicht sie in Echtzeit.
- Setzt genau ein Ergebnis-Signal auf `true`:
  - `equal`: wenn `a == b`
  - `greater`: wenn `a > b`
  - `less`: wenn `a < b`

**Testbench: `ComparatorSim.scala`**

```scala
import spinal.core._
import spinal.sim._
import spinal.core.sim._

object ComparatorSim {
  def main(args: Array[String]): Unit = {
    SimConfig.withWave.compile(new Comparator(4)).doSim { dut =>
      dut.io.a #= 5
      dut.io.b #= 5
      sleep(1)
      assert(dut.io.equal.toBoolean)

      dut.io.a #= 7
      dut.io.b #= 4
      sleep(1)
      assert(dut.io.greater.toBoolean)

      dut.io.a #= 2
      dut.io.b #= 8
      sleep(1)
      assert(dut.io.less.toBoolean)

      simSuccess()
    }
  }
}
```


**Verilog-Ausgabe: `ComparatorVerilog.scala`**

```scala
import spinal.core._

object ComparatorVerilog {
  def main(args: Array[String]): Unit = {
    SpinalVerilog(new Comparator(4))
  }
}
```


**Verwendung**

```bash
sbt compile
sbt "runMain ComparatorSim"
sbt "runMain ComparatorVerilog"
```

Ergebnis: Die Datei `Comparator.v` wird generiert, und die Testbench prüft die Vergleichsfunktionen.

---
## Zähler

Ein Zähler zählt bei jedem Takt um 1 nach oben. Er kann in vielen Anwendungen eingesetzt werden, z. B. als Zeitgeber, Schleifenzähler oder zur Adressierung.

**Aufbau des Moduls**

```scala
class Counter(width: Int) extends Component {
  val io = new Bundle {
    val enable = in Bool()
    val reset  = in Bool()
    val value  = out UInt(width bits)
  }

  val count = Reg(UInt(width bits)) init(0)

  when(io.reset) {
    count := 0
  } .elsewhen(io.enable) {
    count := count + 1
  }

  io.value := count
}
```
**Was macht das Modul?**

- `enable`: Wenn aktiv, zählt der Zähler hoch.
- `reset`: Wenn aktiv, wird der Zähler auf 0 gesetzt.
- `value`: Der aktuelle Zählerwert.

**Testbench: `CounterSim.scala`**

```scala
import spinal.core._
import spinal.sim._
import spinal.core.sim._

object CounterSim {
  def main(args: Array[String]): Unit = {
    SimConfig.withWave.compile(new Counter(4)).doSim { dut =>
      dut.clockDomain.forkStimulus(10)

      dut.io.reset #= true
      dut.io.enable #= false
      dut.clockDomain.waitSampling()

      dut.io.reset #= false
      dut.io.enable #= true

      for (i <- 0 until 5) {
        dut.clockDomain.waitSampling()
        println(s"Zählerwert = ${dut.io.value.toBigInt}")
      }

      simSuccess()
    }
  }
}
```
**Verilog-Ausgabe: `CounterVerilog.scala`**

```scala
import spinal.core._

object CounterVerilog {
  def main(args: Array[String]): Unit = {
    SpinalVerilog(new Counter(4))
  }
}
```
**Verwendung**

```bash
sbt compile
sbt "runMain CounterSim"
sbt "runMain CounterVerilog"
```

**Ergebnis:**
Die Datei `Counter.v` wird generiert. In der Simulation zählt der Wert bei `enable = true` hoch.

---

## Taktteiler (Clock Divider)

Ein Taktteiler erzeugt aus einem schnellen Eingangstakt einen langsameren Ausgangstakt, indem er Takte zählt und z. B. nur jedes 256. Signal durchlässt.

**Aufbau des Moduls**

```scala
class ClockDivider(divisorWidth: Int) extends Component {
  val io = new Bundle {
    val clkOut = out Bool()
  }

  val counter = Reg(UInt(divisorWidth bits)) init(0)
  counter := counter + 1
  io.clkOut := counter.msb
}
```
**Was macht das Modul?**

- `counter`: Zählt kontinuierlich bei jedem Takt.
- `msb`: Der höchste Bitwert des Zählers (Most Significant Bit) wird als geteilter Takt ausgegeben.
- **Beispiel**: Bei `divisorWidth = 8` ergibt sich ein Teiler von 256 (halbe Periode = 128 Takte).

**Testbench: `ClockDividerSim.scala`**

```scala
import spinal.core._
import spinal.sim._
import spinal.core.sim._

object ClockDividerSim {
  def main(args: Array[String]): Unit = {
    SimConfig.withWave.compile(new ClockDivider(8)).doSim { dut =>
      dut.clockDomain.forkStimulus(10)

      for (i <- 0 until 300) {
        dut.clockDomain.waitSampling()
        println(s"Takt $i: clkOut = ${dut.io.clkOut.toBoolean}")
      }

      simSuccess()
    }
  }
}
```

**Verilog-Ausgabe: `ClockDividerVerilog.scala`**

```scala
import spinal.core._

object ClockDividerVerilog {
  def main(args: Array[String]): Unit = {
    SpinalVerilog(new ClockDivider(8))
  }
}
```

**Verwendung**

```bash
sbt compile
sbt "runMain ClockDividerSim"
sbt "runMain ClockDividerVerilog"
```

Das erzeugt:
- `ClockDivider.v`: die Verilog-Datei
- und zeigt die Simulation mit `clkOut`, der etwa alle 128 Takte wechselt.

---

## PWM

Dies ist ein einfaches SpinalHDL-Projekt, das ein parametrierbares PWM-Modul (Pulsweitenmodulation) implementiert. Es enthält:

- eine Hardwarebeschreibung (`Pwm.scala`)
- eine Testbench (`PwmSim.scala`)
- eine Verilog-Ausgabe (`PwmVerilog.scala`)
- und eine verständliche Erklärung des Funktionsprinzips

**Projektstruktur**

```
pwm-spinalhdl/
├── build.sbt
├── project/
│   └── build.properties
├── src/
│   ├── main/
│   │   └── scala/
│   │       ├── Pwm.scala           ← [1] PWM-Modul
│   │       └── PwmVerilog.scala    ← [3] Verilog-Ausgabe
│   └── test/
│       └── scala/
│           └── PwmSim.scala        ← [2] Simulation
└── README.md
```

**Erklärung des PWM-Moduls**

Das PWM-Modul erzeugt ein Signal, das schnell zwischen **an (1)** und **aus (0)** wechselt.  
Wie lange das Signal „an“ bleibt, hängt vom **Duty-Cycle** ab – einem Eingabewert, der angibt, wie viel Prozent der Zeit das Signal „an“ sein soll.

**Aufbau des Moduls**

```scala
class Pwm(width: Int) extends Component {
  val io = new Bundle {
    val enable = in Bool()
    val duty   = in UInt(width bits)
    val pwmOut = out Bool()
  }

  val counter = Reg(UInt(width bits)) init(0)
  counter := counter + 1
  io.pwmOut := io.enable && (counter < io.duty)
}
```

**Was macht das Modul?**

- `width`: Gibt an, wie genau das PWM-Signal sein soll (z. B. 8 Bit → Werte von 0 bis 255).
- `enable`: Schaltet das PWM-Signal ein oder aus.
- `duty`: Bestimmt, wie lange das Signal „an“ sein soll (je höher der Wert, desto länger).
- `counter`: Zählt von 0 bis zum Maximalwert und beginnt dann wieder von vorn.
- `pwmOut`: Wird „an“, solange `counter < duty`.

###  Beispiel (bei 8 Bit Auflösung)

- `duty = 0` → Signal ist immer aus
- `duty = 128` → Signal ist 50 % der Zeit an
- `duty = 255` → Signal ist immer an

Das Modul vergleicht einen Zähler mit einem Zielwert (`duty`).  
Solange der Zähler kleiner ist, ist das Signal **an**  danach **aus**.  
Dieser Zyklus wiederholt sich ständig.

  **[1] `src/main/scala/Pwm.scala` (Code wie oben)**

Siehe oben unter „Aufbau des Moduls“.

**[2] `src/test/scala/PwmSim.scala`**

```scala
import spinal.core._
import spinal.sim._
import spinal.core.sim._

object PwmSim {
  def main(args: Array[String]): Unit = {
    SimConfig
      .withWave
      .compile(new Pwm(8)) // 8-Bit PWM
      .doSim { dut =>
        dut.clockDomain.forkStimulus(10)

        dut.io.enable #= true
        dut.io.duty   #= 128 // 50% Duty Cycle

        for (cycle <- 0 until 300) {
          dut.clockDomain.waitSampling()
        }

        simSuccess()
      }
  }
}
```
**`[3]PwmVerilog.scala`**

```scala
import spinal.core._

object PwmVerilog {
  def main(args: Array[String]): Unit = {
    SpinalVerilog(new Pwm(8))
  }
}
```



**`build.sbt`**

```scala
name := "pwm-spinalhdl"

version := "0.1"

scalaVersion := "2.13.12"

libraryDependencies ++= Seq(
  "com.github.spinalhdl" %% "spinalhdl-core" % "1.9.1",
  "com.github.spinalhdl" %% "spinalhdl-sim"  % "1.9.1" % Test
)
```



**Projekt kompilieren und starten**



```bash
sbt compile
```

```bash
sbt "runMain PwmVerilog"
```

```bash
sbt "runMain PwmSim"
```


**Ergebnis**

- Wir erhalten ein synthetisierbares PWM-Modul  
- Wir können das Verhalten direkt simulieren  
- Der generierte Verilog-Code (`Pwm.v`) ist für FPGA/ASIC verwendbar
