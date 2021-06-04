package software.amazon.smithy.crt.python

import java.util.Optional
import software.amazon.smithy.model.shapes.StructureShape
import software.amazon.smithy.model.traits.Trait.getIdiomaticTraitName
import java.lang.StringBuilder

const val POINTER_TRAIT = "com.aws.ffi#ctype"

fun <T> Optional<T>.orNull(): T? = this.orElse(null)

fun processInput(struct: StructureShape?): String? {
    if (struct == null) {
        return null
    }

    val pointer = struct.findTrait(POINTER_TRAIT).orNull()
    if (pointer != null) {
        println(pointer.toNode())
        println("im hereadfdslgnfo")
        println(pointer.toNode().expectObjectNode().expectStringMember("typename"))
        println(getIdiomaticTraitName(POINTER_TRAIT))
        return ""
    }

    var str = StringBuilder();
    struct.allMembers.forEach {
        println(it.value)
    }

    println(str.toString())
    return ""
}